# Music Profile Analytics

The Music Profile Analytics Dashboard is a Streamlit application that analyzes a user’s Spotify listening history and presents the results through interactive visualizations and simple machine-learning models. Building this project sharpened my skills across the **entire analytics workflow**—from data collection and cleaning to exploratory analysis, feature engineering, modeling, and communication.

## Why I Built This

I wanted a concise yet technically rich project that:

1. **Shows end-to-end data‐science thinking** on a real-world dataset that recruiters can recognize.  
2. Demonstrates that I can build **data products**—not just notebooks—by shipping a working web app.  
3. Pushes the limits of standard Spotify metadata after the platform restricted access to advanced audio features (danceability, valence, energy, etc.).  

## What I Learned

| Area                       | Practical Takeaways                                                                                                             |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| **API Integration**        | Implemented OAuth with the Spotify Web API; handled rate limits and token caching; secured credentials via `.env` and `.gitignore`. |
| **Data Wrangling**         | Normalized nested JSON into tabular form with Pandas; joined Spotify data with Last.fm artist metadata; handled missing values.   |
| **Feature Engineering**    | Created custom fields such as *Taste Diversity Score* and “Hidden Gems” filters; encoded categorical data for clustering.        |
| **Exploratory Analysis**   | Used Plotly for ad-hoc EDA—genre distributions, language detection, release-year timelines—to drive hypothesis formation.        |
| **Unsupervised Learning**  | Applied K-Means to group tracks by duration and popularity; experimented with cluster counts and feature scaling (StandardScaler). |
| **Visualization & UX**     | Designed a multi-tab Streamlit dashboard; kept plots interactive and consistent through a styling helper; embedded Spotify players.|
| **Product Thinking**       | Balanced technical depth with usability—download buttons, playlist generator, and business-style insights that non-technical users understand. |
| **Limitations & Roadmap**  | Documented how missing audio‐feature endpoints affected analysis; proposed future work using open-source embeddings and additional platforms. |

These experiences mirror the data-science tasks I would handle at an internship: collecting raw data, turning it into insight, and shipping a deliverable that others can use.

## Key Features

* **Multi-Range Data Pull** – Retrieves top tracks for 4 weeks, 6 months, and all-time windows.  
* **Interactive Visuals** – Genre, language, release year, and popularity charts with hover details.  
* **Taste Diversity Score** – Custom metric combining genre, language, release-year span, and popularity rarity.  
* **K-Means Clustering** – Groups tracks by duration & popularity; visualized on a scatter plot.  
* **Playlist Generator** – Builds a private Spotify playlist of the displayed tracks in one click.  
* **Hidden Gems Finder** – Surfaces clean, low-popularity songs that might deserve more playtime.  

## Limitations and Future Work

Spotify now restricts audio feature endpoints (`danceability`, `valence`, etc.). I worked around this by focusing on available metadata and external APIs (e.g., Last.fm). Next steps:

1. **Audio Embeddings** – Generate vector representations with open-source models to enrich clustering.  
2. **Cross-Platform Support** – Add YouTube Music and SoundCloud to broaden analysis beyond Spotify.  
3. **Recommendation Engine** – Leverage similarity metrics to suggest brand-new songs, not just analyze existing ones.  
4. **Automated Reporting** – Export user-friendly PDF or HTML summaries for sharing.
