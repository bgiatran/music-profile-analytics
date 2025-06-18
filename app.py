"""
Spotify Listening Insight Dashboard
Author: Bria Tran
Date: June 17th, 2025
Purpose: This dashboard is designed to help Spotify users visualize and explore
         their music listening habits. It authenticates with Spotify using OAuth,
         pulls the user's top tracks, and presents insights using charts and
         tables. Data includes genre, language, popularity, duration, and more.
         You can also auto-generate a playlist from your favorite tracks.
"""

# 1. Imports and Environment Setup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import plotly.express as px
from langdetect import detect, DetectorFactory
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import requests
import pycountry

# ── Load API keys from .env file ────────────────────────────────────────────────
CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8888/callback"  # works locally and ignored by cloud
LAST_CLIENT_ID = st.secrets["LAST_CLIENT_ID"]

# ── 2. Spotify OAuth Setup ──────────────────────────────────────────────────────
# Set the scope of permissions we want from the user.
# 'user-top-read' lets us access the user's top tracks/artists,
# and 'playlist-modify-private' allows us to create private playlists on their behalf.
scope = "user-top-read playlist-modify-private"

# Set up the Spotify OAuth authorization manager.
# This handles the process of logging the user in and getting a valid access token.
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    show_dialog=True,
    cache_path=".cache"
)

# Create a Spotipy client using the auth manager above.
# This 'sp' object will be used to interact with the Spotify Web API.
sp = spotipy.Spotify(auth_manager=auth_manager)

# ── 3. Page Configuration ───────────────────────────────────────────────────────
# Configure the Streamlit page.
# We give it a custom title and use a wide layout for better space usage.
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

# Add a custom header to the top of the app using HTML and inline CSS.
# This helps the dashboard feel more branded and user-friendly.
st.markdown("""
    <div style='background-color:#111827; padding:8px 16px; color:white; font-size:14px;
                display:flex; justify-content:space-between; align-items:center;'>
        <span><strong>Spotify Listening Insight Dashboard</strong></span>
        <span style='font-size:12px; opacity:0.8;'>Visualize your top tracks, genres, languages, and more</span>
    </div>
""", unsafe_allow_html=True)

# ── 4. Authenticate and Load User ───────────────────────────────────────────────
# Try to fetch the current user's profile info from the Spotify API.
# This verifies that our authentication worked and we can access the user's data.
try:
    user = sp.current_user() # Get basic profile data (e.g., name, profile pic, ID)

    # If successful, display the user's profile image in the top right corner of the app.
    # This makes the app feel more personalized and confirms who is logged in.
    st.markdown(
        f"<div style='position:fixed; top:10px; right:15px; font-size:14px;'>"
        f"<img src='{user['images'][0]['url'] if user['images'] else ''}' width='30' height='30' "
        f"style='border-radius:50%; vertical-align:middle;'></div>",
        unsafe_allow_html=True
    )

# If something goes wrong during the authentication (e.g. token expired, user cancels login),
# show an error message and stop the app so it doesn't crash later from missing user data.
except Exception as e:
    st.error(f"Authentication failed: {e}")
    st.stop()

# ── 5. Helper: Get Artist Country from Last.fm ───────────────────────────────────
# Tries to detect the artist's country of origin using Last.fm's API.
# It parses the artist bio and looks for any country names inside it.
def get_artist_country_lastfm(artist_name):
    try:
        # Call the Last.fm API to get artist info, using their name
        url = (f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo"
               f"&artist={artist_name}&api_key={LAST_CLIENT_ID}&format=json")
        res = requests.get(url).json()

        # Extract the artist biography text from the JSON response
        bio = res.get("artist", {}).get("bio", {}).get("content", "")

        # Check if any official country name appears in the biography text
        for country in [c.name for c in pycountry.countries]:
            if country.lower() in bio.lower():
                return country
        # If no country match is found, return "Unknown"
        return "Unknown"
    except Exception:
        # If anything goes wrong (e.g., API error), just return "Unknown"
        return "Unknown"

# ── 6. Chart Styling Helper ─────────────────────────────────────────────────────
# Applies consistent layout and hover styling to Plotly charts.
# This makes the graphs look cleaner and more readable in the dashboard.
def style_chart(fig):
    fig.update_layout(height=300, margin=dict(t=40, b=40))
    fig.update_xaxes(tickangle=45, automargin=True)
    fig.update_traces(hovertemplate="%{x}: %{y}<extra></extra>")
    return fig

# ── 7. Sidebar: Time Range Selector ─────────────────────────────────────────────
# Create a dropdown in the sidebar to let users pick which time range they want to analyze.
# Spotify lets us pull data from short_term (1 month), medium_term (6 months), or long_term (all time).
time_range = st.sidebar.selectbox(
    "Select Time Range",
    [("short_term", "Last 4 Weeks"),
     ("medium_term", "Last 6 Months"),
     ("long_term", "All Time")],
    format_func=lambda x: x[1] # Display friendly label in UI, not raw keys
)[0] # We only need the first element (e.g., "short_term") to use in the API

# ── 8. Fetch Top Tracks ─────────────────────────────────────────────────────────
# Make language detection deterministic by fixing the random seed
# Fetches the user's top 20 tracks from Spotify and processes each one
# to extract useful metadata for display and analysis.
DetectorFactory.seed = 0

def fetch_tracks(time_range):
    try:
        top_tracks = sp.current_user_top_tracks(limit=20, time_range=time_range)
        if not top_tracks["items"]:
            return pd.DataFrame()

        rows = []
        for item in top_tracks["items"]: # Get artist information (we use the first artist listed for each track)
            artist_id = item["artists"][0]["id"]
            artist_info = sp.artist(artist_id)
            genres = artist_info.get("genres", [])

            # Try to detect the language of the track name + artist name
            try:
                lang_input = f"{item['name']} {item['artists'][0]['name']}"
                language = detect(lang_input)
            except Exception:
                language = "unknown"

            # Try to detect artist country using Last.fm bio
            country = get_artist_country_lastfm(item["artists"][0]["name"])

            # Append all extracted data for this track into the rows list
            rows.append({
                "Track Name": item["name"],
                "Artist": item["artists"][0]["name"],
                "Album": item["album"]["name"],
                "Genre": genres[0] if genres else "Unknown",
                "Language": language,
                "Duration (min)": round(item["duration_ms"] / 60000, 2),
                "Popularity": item["popularity"],
                "Explicit": "Explicit" if item["explicit"] else "Clean",
                "Release Year": item["album"]["release_date"][:4],
                "Country": country
            })

        # Convert the list of rows into a pandas DataFrame for easy analysis and plotting
        return pd.DataFrame(rows)

    except Exception as e:
        # If anything fails (e.g. API error), show a Streamlit error and return empty data
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# ── 9. Load Data ────────────────────────────────────────────────────────────────
# Preload the user's top tracks from all 3 time ranges:
# short_term = last 4 weeks, medium_term = last 6 months, long_term = all time
df_short  = fetch_tracks("short_term")
df_medium = fetch_tracks("medium_term")
df_long   = fetch_tracks("long_term")

# Also fetch the top tracks based on the currently selected time range (from sidebar)
df = fetch_tracks(time_range)

if df.empty:
    st.warning("No data found.")
    st.stop()

# ── 10. Tabbed Layout ───────────────────────────────────────────────────────────
# Use Streamlit's tab layout to separate content into 4 main categories
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Charts", "Playlist & Clustering", "Hidden Gems"]
)

# 10a. Overview tab
with tab1:
    # Allow user to download their top tracks as a CSV
    st.download_button("Download Track Data as CSV",
                       df.to_csv(index=False), file_name="top_tracks.csv")

    # Show the full track DataFrame for transparency and browsing
    st.subheader("Top Tracks Overview")
    st.dataframe(df, use_container_width=True)

# 10b. Charts tab
# Interactive visual analysis of top tracks
with tab2:
    with tab2:
        # Subdivide the Charts section into 5 sub-tabs, each focusing on a specific type of analysis.
        subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
            "Track Stats", "Cultural Insights", "Time & Trends",
            "Artists & Albums", "Advanced Analysis"
        ])

        # ── Track Stats ───────────────────────────────────────────────
        # Basic statistics like most popular tracks, track durations, and explicit content breakdown.
        with subtab1:
            col1, col2 = st.columns(2)

            # Bar chart to show most popular songs among the user’s top 20.
            # Colored by artist to see which artists contribute most to the user's popular picks.
            with col1:
                st.subheader("Top Tracks by Popularity")
                st.plotly_chart(style_chart(
                    px.bar(df, x="Track Name", y="Popularity", color="Artist")
                ), use_container_width=True)

            # Bar chart of longest tracks by duration
            with col2:
                st.subheader("Top Tracks by Duration (min)")
                st.plotly_chart(style_chart(
                    px.bar(df, x="Track Name", y="Duration (min)", color="Artist")
                ), use_container_width=True)

            # Pie chart to show what % of songs are marked Explicit (vs. Clean) by Spotify.
            st.subheader("Overall Explicit Content Breakdown")
            explicit_counts = df["Explicit"].value_counts()
            fig_explicit = px.pie(
                names=explicit_counts.index,
                values=explicit_counts.values,
                hole=0.4 # Makes it a donut chart
            )
            st.plotly_chart(style_chart(fig_explicit), use_container_width=True)

        # ── Cultural Insights ─────────────────────────────────────────
        # Here we dive into genres, languages, and how they relate to explicit content.
        with subtab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Genre Distribution")
                # Pie chart to show which genres dominate the user's listening habits.
                genre_counts = df["Genre"].value_counts()
                fig_genres = px.pie(names=genre_counts.index, values=genre_counts.values)
                st.plotly_chart(style_chart(fig_genres), use_container_width=True)

            with col2:
                st.subheader("Detected Song Languages")
                # I used a language detection model on track/artist names earlier.
                # This helps visualize how international the user's music taste is.
                lang_counts = df["Language"].value_counts()
                fig_lang = px.bar(
                    x=lang_counts.index,
                    y=lang_counts.values,
                    labels={"x": "Language", "y": "Track Count"}
                )
                st.plotly_chart(style_chart(fig_lang), use_container_width=True)

            st.subheader("Explicitness by Language")
            # Compare explicit vs. clean songs *by language*, e.g. is English more explicit than Spanish?
            lang_exp = df.groupby(["Language", "Explicit"]).size().reset_index(name="Count")
            fig_lang_exp = px.bar(
                lang_exp,
                x="Language", y="Count",
                color="Explicit",
                barmode="group",
                title="Explicit vs Clean Tracks by Language"
            )
            st.plotly_chart(style_chart(fig_lang_exp), use_container_width=True)

        # ── Time & Trends ─────────────────────────────────────────────
        # Looks at how your top tracks evolved over time in terms of release year and genre.
        with subtab3:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Release Year Distribution")
                # How old are your favorite tracks? A bar chart showing number of songs per year.
                release_counts = df["Release Year"].value_counts().sort_index()
                fig_release = px.bar(
                    x=release_counts.index, y=release_counts.values,
                    labels={"x": "Year", "y": "Track Count"}
                )
                st.plotly_chart(style_chart(fig_release), use_container_width=True)

            with col2:
                st.subheader("Explicit Tracks Over Time")
                # Do you listen to more explicit content in recent years? This grouped chart shows that.
                year_exp = df.groupby(["Release Year", "Explicit"]).size().reset_index(name="Count")
                fig_year_exp = px.bar(
                    year_exp, x="Release Year", y="Count",
                    color="Explicit", barmode="group"
                )
                st.plotly_chart(style_chart(fig_year_exp), use_container_width=True)

            st.subheader("Listening Evolution by Genre")
            # Compare genre breakdown across 3 time periods.
            # Great for identifying shifts in taste (e.g. more EDM recently).
            fig_evo = go.Figure()
            for label, dataset in zip(["Short", "Medium", "Long"], [df_short, df_medium, df_long]):
                genre_cnt = dataset["Genre"].value_counts()
                fig_evo.add_trace(go.Bar(x=genre_cnt.index, y=genre_cnt.values, name=label))
            fig_evo.update_layout(barmode="group")
            st.plotly_chart(style_chart(fig_evo), use_container_width=True)

        # ── 🧑‍🎤 Artists & Albums ────────────────────────────────────────
        # This section highlights the most popular and frequent artists/albums in your top tracks.
        with subtab4:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top Artists by Average Popularity")
                # For each artist, calculate their average popularity score across all your top tracks.
                artist_popularity = df.groupby("Artist")["Popularity"].mean().sort_values(ascending=False).reset_index()
                fig_artist = px.bar(
                    artist_popularity.head(10),
                    x="Artist", y="Popularity",
                    color="Popularity",
                    title="Most Popular Artists (on Avg)"
                )
                st.plotly_chart(style_chart(fig_artist), use_container_width=True)

            with col2:
                st.subheader("Most Frequent Artists")
                # Which artists appear the most in your top tracks? (Not necessarily most popular.)
                artist_freq = df["Artist"].value_counts().reset_index()
                artist_freq.columns = ["Artist", "Count"]
                fig_freq = px.bar(
                    artist_freq.head(10), x="Artist", y="Count",
                    color="Count",
                    title="Artists You Listen to Most"
                )
                st.plotly_chart(style_chart(fig_freq), use_container_width=True)

            col3, col4 = st.columns(2)
            with col3:
                st.subheader("Top Albums by Frequency")
                # What albums do you have the most tracks from in your top list?
                album_counts = df["Album"].value_counts().reset_index()
                album_counts.columns = ["Album", "Count"]
                fig_albums = px.bar(
                    album_counts.head(10),
                    x="Album", y="Count",
                    color="Count",
                    title="Albums with Most Tracks in Your Top List"
                )
                st.plotly_chart(style_chart(fig_albums), use_container_width=True)

            with col4:
                st.subheader("Genres with Highest Popularity")
                # Which genres tend to have higher average popularity in your library?
                genre_popularity = df.groupby("Genre")["Popularity"].mean().sort_values(ascending=False).reset_index()
                fig_genre_pop = px.bar(
                    genre_popularity.head(10),
                    x="Genre", y="Popularity",
                    color="Popularity",
                    title="Top Performing Genres"
                )
                st.plotly_chart(style_chart(fig_genre_pop), use_container_width=True)

        # ── 🧪 Advanced Analysis ─────────────────────────────────────────
        # Final layer of insights: more technical plots for deeper patterns.
        with subtab5:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Popularity vs Release Year")
                # Scatter plot to explore how popularity relates to release year (grouped by genre).
                fig_scatter = px.scatter(
                    df, x="Release Year", y="Popularity",
                    color="Genre", hover_name="Track Name"
                )
                st.plotly_chart(style_chart(fig_scatter), use_container_width=True)

            with col2:
                st.subheader("Genre vs Explicitness Heatmap")
                # Heatmap that shows which genres have more explicit or clean content overall.
                genre_explicit = df.groupby(["Genre", "Explicit"]).size().reset_index(name="Count")
                fig_heatmap = px.density_heatmap(
                    genre_explicit, x="Genre", y="Explicit", z="Count",
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(style_chart(fig_heatmap), use_container_width=True)

            # Finally, explore how track length and popularity correlate
            st.subheader("Correlation Matrix")
            corr_data = df[["Duration (min)", "Popularity"]].corr()
            fig_corr = px.imshow(corr_data, text_auto=True, color_continuous_scale="Viridis")
            st.plotly_chart(style_chart(fig_corr), use_container_width=True)

# 10c. Playlist and Clustering tab
with tab3:
    # Split the page into three vertical sections: one for diversity scoring,
    # one for playlist creation, and one for similarity-based clustering.
    col_a, col_b, col_c = st.columns(3)

    # Taste diversity score
    with col_a:
        st.subheader("Taste Diversity Score")

        # This is a custom "taste diversity" metric that scores the variety in a user's top tracks.
        # It's a rough estimate based on how many unique genres, languages, and release years appear.
        # Also considers average popularity — lower average suggests more niche discovery.
        diversity = (
            len(df["Genre"].unique()) * 2 +
            len(df["Language"].unique()) * 2 +
            len(df["Release Year"].unique()) +
            (100 - df["Popularity"].mean())
        )
        # Show the diversity score using Streamlit’s metric widget
        st.metric("Your Diversity Score", f"{int(diversity)} / 100")

    # Playlist builder
    with col_b:
        # Use Streamlit's session_state to track whether a playlist was already created.
        # This prevents duplicate creations and allows us to reuse the playlist URL.
        if "playlist_created" not in st.session_state:
            st.session_state.playlist_created = False
            st.session_state.playlist_url = None

        # Only show the playlist creation UI if one hasn’t already been made in this session
        if not st.session_state.playlist_created:
            st.subheader("Create Your Playlist")
            track_uris = []

            # For each song in the top track list, search for its URI using Spotify’s search endpoint
            for _, r in df.iterrows():
                res = sp.search(q=f"{r['Track Name']} {r['Artist']}", type="track", limit=1)
                if res["tracks"]["items"]:
                    track_uris.append(res["tracks"]["items"][0]["uri"])

            # Once we have all URIs, allow the user to click a button to create the playlist
            if track_uris and st.button("+ Create Spotify Playlist"):
                playlist = sp.user_playlist_create(
                    user=user["id"],
                    name="My Favorite Tracks",
                    public=False,
                    description="Auto-generated from Spotify Insight Dashboard"
                )
                # Add all the songs to the newly created playlist
                sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

                # Get the playlist's public URL and store it in session_state for later use
                playlist_url = playlist["external_urls"]["spotify"]
                st.session_state.playlist_created = True
                st.session_state.playlist_url = playlist_url

        # If a playlist has already been created, show an embedded Spotify preview player
        if st.session_state.playlist_created and st.session_state.playlist_url:
            embed_url = st.session_state.playlist_url.replace(
                "https://open.spotify.com/playlist/",
                "https://open.spotify.com/embed/playlist/"
            )
            st.markdown(f"""
                <div style="margin-top: 1rem; margin-bottom: 2rem;">
                    <iframe src="{embed_url}?theme=0" width="100%" height="500"
                            frameborder="0" allowtransparency="true" allow="encrypted-media"
                            style="border-radius:12px; background-color: transparent;">
                    </iframe>
                </div>
            """, unsafe_allow_html=True)

    # Clustering chart
    with col_c:
        st.subheader("Track Similarity Clustering")

        # We’ll use only two features: duration and popularity.
        # In a real system we could include more audio features like valence, tempo, etc.
        feat = df[["Duration (min)", "Popularity"]].copy()

        # Normalize the data so KMeans works properly (prevents scale dominance)
        scaled = StandardScaler().fit_transform(feat)

        # Apply KMeans clustering to group tracks into 3 similarity clusters
        kmeans = KMeans(n_clusters=3, random_state=42).fit(scaled)
        df["Cluster"] = kmeans.labels_ # Add cluster label to each track in the DataFrame

        # Visualize the clusters in a scatterplot: Duration vs. Popularity
        st.plotly_chart(style_chart(
            px.scatter(df, x="Duration (min)", y="Popularity",
                       color="Cluster", hover_name="Track Name")
        ), use_container_width=True)

# 10d. Hidden Gems tab
with tab4:
    st.subheader("Hidden Gems (Popularity < 40, Clean lyrics)")

    # Filter the top tracks to only include songs that meet all of these:
    # - Popularity is below 40 (more likely unknown or underrated)
    # - Lyrics are clean (non-explicit)
    # - Genre is known (ignore 'Unknown' for better recommendations)
    hidden = df[(df["Popularity"] < 40) &
                (df["Explicit"] == "Clean") &
                (df["Genre"] != "Unknown")]
    # Display the list of hidden gems in a table so users can discover new favorites
    st.dataframe(hidden, use_container_width=True)