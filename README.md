# Spotify Listening Insight Dashboard

## Project Overview
The Spotify Listening Insight Dashboard is a web-based data analytics application that allows users to visualize their Spotify listening behavior. By integrating with the Spotify Web API and Last.fm, the dashboard provides personalized insights into music preferences including genres, explicit content trends, language exposure, release year distribution, and track clustering.

This project demonstrates the integration of APIs, data visualization, unsupervised machine learning, and user-centric product design within an interactive Streamlit application.

---

## Technology Stack
| Category       | Technology Used                     | Purpose                                         |
|----------------|--------------------------------------|-------------------------------------------------|
| Programming    | Python                              | Core development language                       |
| Framework      | Streamlit                           | Interactive web application framework           |
| API Integration| Spotify Web API, Last.fm API        | Fetch user listening data and artist metadata   |
| Authentication | Spotipy with OAuth2                 | User account authentication and token handling  |
| Data Handling  | Pandas                              | Data transformation and management              |
| Visualization  | Plotly                              | Interactive chart rendering                     |
| Language Detection | langdetect                      | Infer song language from metadata               |
| Machine Learning| scikit-learn (KMeans)               | Clustering tracks based on features             |
| Country Lookup | pycountry, requests                 | Extract artist origin from bio and metadata     |

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bgiatran/music-profile-analytics.git
cd music-profile-analytics
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Streamlit Secrets
Create a `.streamlit/secrets.toml` file with the following content:
```toml
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
LAST_CLIENT_ID = "your_lastfm_api_key"
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## Application Structure and Feature Walkthrough

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Overview Tab</h3>
    <p><strong>Function:</strong> Displays a full table of the user's top tracks over a selected time range (last 4 weeks, 6 months, all time). Users can download this as a CSV.</p>
    <p><strong>Why it matters:</strong> This acts as a data transparency layer — it gives users full access to the raw insights driving the dashboard’s charts. It’s also useful for power users or analysts who want to manipulate or archive their own data independently.</p>
    <p><strong>Practical Use Cases:</strong></p>
    <ul>
      <li>Data export for personal archiving or further analysis</li>
      <li>Validation for research studies or music psychology projects</li>
      <li>Entry point for comparing across time ranges or users</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (86).png" alt="Overview Tab Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <img src="./images/Screenshot (87).png" alt="Track Stats Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
  <div style="flex: 1;">
    <h3>Track Stats</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Most popular tracks</li>
      <li>Longest tracks</li>
      <li>Share of explicit vs. clean content</li>
    </ul>
    <p><strong>Why it matters:</strong> Users can quickly see what songs dominate their behavior, whether they lean toward long form vs. short form music, and how “safe” their playlist is (e.g., for family or public spaces).</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>Playlist planning for events, kids, or public playback</li>
      <li>Discovering which favorites are also commercial hits</li>
      <li>Identifying “attention grabber” songs in your habits</li>
    </ul>
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Cultural Insights</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Genre breakdown</li>
      <li>Language detection</li>
      <li>Explicit content by language</li>
    </ul>
    <p><strong>Why it matters:</strong> Highlights exposure to cultural and linguistic diversity. Reveals unconscious biases or global curiosity in music preferences.</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>See how much non-English content you're consuming</li>
      <li>Artists/marketers: which languages & genres are trending</li>
      <li>For inclusive UX: understanding user diversity</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (88).png" alt="Cultural Insights Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <img src="./images/Screenshot (89).png" alt="Time & Trends Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
  <div style="flex: 1;">
    <h3>Time & Trends</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Track release year distribution</li>
      <li>Explicit content trends over time</li>
      <li>Genre preferences across short/medium/long term</li>
    </ul>
    <p><strong>Why it matters:</strong> Answers questions like: "Do I listen to old or new music?", "Have my tastes evolved?", or "Do I trend toward cleaner music over time?"</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>Spotting seasonal genre trends</li>
      <li>Tracking behavior over time</li>
      <li>Emerging artists watching niche adoption patterns</li>
    </ul>
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Artists & Albums</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Top artists by average popularity</li>
      <li>Most frequent artists</li>
      <li>Top albums</li>
      <li>Most popular genres by score</li>
    </ul>
    <p><strong>Why it matters:</strong> Understands listener loyalty, artist impact, and genre trend alignment. Useful for recognizing patterns in favorites.</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>For A&R reps or fan engagement teams</li>
      <li>Playlist creators optimizing artist mix</li>
      <li>Understanding repeat listen behaviors</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (90).png" alt="Artists & Albums Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <img src="./images/Screenshot (91).png" alt="Advanced Analysis Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>
  <div style="flex: 1;">
    <h3>Advanced Analysis</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Release year vs. popularity scatterplots</li>
      <li>Genre vs. explicitness heatmaps</li>
      <li>Correlation matrix (e.g., popularity vs. track length)</li>
    </ul>
    <p><strong>Why it matters:</strong> Great for data-literate users to identify cross-dimensional trends and outliers. Surfaces deeper insights beyond surface stats.</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>Musicology or streaming behavior research</li>
      <li>Understanding clean vs. explicit success ratios</li>
      <li>Correlating length, popularity, and genre intent</li>
    </ul>
  </div>
</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">

  <div style="flex: 1;">
    <h3>Playlist & Clustering Tab</h3>

  <p><strong>What it includes:</strong></p>
  <ul>
    <li><strong>Taste Diversity Score</strong>: a custom metric quantifying how adventurous a listener is</li>
    <li><strong>Spotify Playlist Creator</strong>: generates a real playlist from top tracks</li>
    <li><strong>Clustering Chart</strong>: groups similar tracks by duration and popularity</li>
  </ul>

  <p><strong>Why it matters:</strong>  
  This tab shifts the focus from analysis to <em>interaction</em>. It offers gamified self-reflection (diversity score), auto-playlist creation, and clustering to show hidden structure in your listening behavior (e.g., fast & popular vs. long & niche).</p>

  <p><strong>Real-world use:</strong></p>
  <ul>
    <li>Generate quick, personalized playlists for fans, DJs, or study/work sessions</li>
    <li>See how diverse or “narrow” your listening taste is over time</li>
    <li>Discover themed song clusters you hadn’t noticed before</li>
  </ul>
  </div>

  <div style="flex: 1;">
    <img src="./images/Screenshot (92).png" alt="Playlist & Clustering Screenshot" style="max-width: 100%; border-radius: 8px;" />
  </div>

</div>

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <img src="./images/Screenshot (93).png" alt="Hidden Gems Screenshoot" style="max-width: 100%; border-radius: 8px;" />
  </div>
  <div style="flex: 1;">
    <h3>Hidden Gems Tab</h3>

  <p><strong>What it showss:</strong></p>
  <ul>
    <li><strong>Popularity under 40<</strong></li>
    <li><strong>Non-explicit</strong> (family-friendly)</li>
    <li><strong>Known genre assigne</strong></li>
  </ul>

  <p><strong>Why it matters:</strong>  
  This helps users uncover underrated, clean, and non-mainstream tracks in their library—songs they may have overlooked that still resonate. These are perfect for recommending to friends or building niche playlists.</p>

  <p><strong>Real-world use:</strong></p>
  <ul>
    <li>Curate playlists of clean, obscure tracks with emotional or thematic value</li>
    <li>Music scouts identifying talent that hasn’t gone viral ye</li>
    <li>Fans re-discovering their own music taste beyond popularity</li>
  </ul>
  </div>

</div>

---

## Project Significance
This project serves as a full-stack data product that integrates:
- Secure user authentication via OAuth
- Real-time API data ingestion and enrichment
- Multi-tabbed dashboard interface with drill-down analytics
- Machine learning to cluster user preferences

---

## Challenges and Learnings
One of the main challenges was the limited access to Spotify's full API feature set. Spotify now restricts audio feature endpoints (`danceability`, `valence`, etc.), which prevents deeper mood or energy-based analysis.

To work around this, I focused on maximizing insights from accessible metadata like popularity, track duration, genre (from artist profiles), and language inference. I also integrated the Last.fm API to enrich artist country data.

**Key Learnings:**
- Deepened understanding of OAuth2 authentication flows and access scope limitations
- Improved skills in API-based data ingestion, error handling, and fallbacks
- Gained hands-on experience in clustering algorithms and interactive visualization for product-level storytelling

---

## Future Work
1. **Audio Embeddings** – Generate vector representations with open-source models to enrich clustering.  
2. **Cross-Platform Support** – Add YouTube Music and SoundCloud to broaden analysis beyond Spotify.  
3. **Recommendation Engine** – Leverage similarity metrics to suggest brand-new songs, not just analyze existing ones.  
4. **Automated Reporting** – Export user-friendly PDF or HTML summaries for sharing.
6. Add support for Spotify audio features (valence, energy, tempo) when access is granted
7. Session tracking and user save history
8. Custom playlist builder with filtering logic
9. Responsive design improvements for mobile access

---

## Use Cases
- Music users analyzing their listening behavior
- Recruiters reviewing technical product portfolios
- PMs and data analysts exploring music streaming trends

---

## Author
**Bria Tran**  
Data Analytics | Product Thinking | Music Intelligence  
GitHub: https://github.com/bgiatran  
LinkedIn: https://linkedin.com/in/bria-tran