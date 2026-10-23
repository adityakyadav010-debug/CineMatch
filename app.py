import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

from recommender import MovieRecommender
from tmdb_api import search_movie


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #172554 50%,
        #111827 100%
    );
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827;
}

/* Main title */
.main-title {
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
    color: #f8fafc;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

/* Section headings */
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
    color: #f8fafc;
}

/* Movie card */
.movie-card {
    padding: 14px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(30,41,59,0.75);
    margin-bottom: 20px;
}

/* Movie title */
.movie-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 5px;
    color: #f8fafc;
}

/* Movie information */
.movie-info {
    color: #cbd5e1;
    font-size: 14px;
}

/* Recommendation badge */
.recommendation-badge {
    padding: 7px 10px;
    border-radius: 8px;
    background: rgba(99,102,241,0.18);
    color: #c7d2fe;
    font-size: 13px;
    margin-top: 10px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(30,41,59,0.65);
    padding: 10px;
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# TMDB CACHE
# ==========================================================

@st.cache_data(ttl=3600)
def get_tmdb_movie(movie_title):

    # First try the original MovieLens title
    movie = search_movie(movie_title)

    if movie:
        return movie

    # If not found, remove year such as "(1997)"
    clean_title = re.sub(
        r"\s*\(\d{4}\)\s*$",
        "",
        movie_title
    ).strip()

    if clean_title != movie_title:

        movie = search_movie(clean_title)

        if movie:
            return movie

    return None


# ==========================================================
# LOAD RECOMMENDER
# ==========================================================

@st.cache_resource
def load_recommender():

    return MovieRecommender()


recommender = load_recommender()


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">🎬 CineMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Personalized Movie Recommendations using Collaborative Filtering'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🎬 CineMatch")

st.sidebar.markdown(
    "### ⚙️ Recommendation Settings"
)

st.sidebar.caption(
    "Choose a user and generate personalized movie recommendations."
)


# ==========================================================
# AVAILABLE USERS
# ==========================================================

try:

    available_users = (
        recommender.user_movie_matrix.index.tolist()
    )

except AttributeError:

    st.error(
        "user_movie_matrix was not found in MovieRecommender."
    )

    st.stop()


# ==========================================================
# USER SELECTION
# ==========================================================

user_id = st.sidebar.selectbox(
    "👤 Select User",
    available_users
)


# ==========================================================
# NUMBER OF RECOMMENDATIONS
# ==========================================================

number_of_recommendations = st.sidebar.slider(
    "🎯 Number of Recommendations",
    min_value=5,
    max_value=15,
    value=10
)


st.sidebar.divider()

st.sidebar.info(
    "Recommendations are generated using "
    "User-Based Collaborative Filtering "
    "and Cosine Similarity."
)


# ==========================================================
# USER PROFILE
# ==========================================================

try:

    stats = recommender.get_user_stats(user_id)

    st.markdown(
        '<div class="section-title">👤 Your Profile</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👤 User ID",
            user_id
        )

    with col2:

        st.metric(
            "🎬 Movies Rated",
            stats["movies_rated"]
        )

    with col3:

        st.metric(
            "⭐ Average Rating",
            stats["average_rating"]
        )

except Exception:

    # If your recommender does not contain get_user_stats()
    # the rest of the application will still work.

    pass


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🎯 Recommendations",
        "👥 Similar Users",
        "⭐ Rating History",
        "📊 Analytics"
    ]
)


# ==========================================================
# TAB 1 - RECOMMENDATIONS
# ==========================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        '🎯 Personalized Recommendations'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Movies recommended based on users with similar "
        "rating patterns."
    )


    # ------------------------------------------------------
    # GENERATE BUTTON
    # ------------------------------------------------------

    if st.button(
        "✨ Generate Recommendations",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🔍 Finding movies you may like..."
        ):

            recommendations = (
                recommender.get_recommendations(
                    user_id,
                    number_of_recommendations
                )
            )


        # --------------------------------------------------
        # NO RECOMMENDATIONS
        # --------------------------------------------------

        if recommendations.empty:

            st.warning(
                "No recommendations found."
            )


        # --------------------------------------------------
        # SHOW RECOMMENDATIONS
        # --------------------------------------------------

        else:

            st.success(
                f"✨ {len(recommendations)} personalized "
                "recommendations generated!"
            )

            st.divider()


            # ------------------------------------------------
            # MOVIE CARDS
            # ------------------------------------------------

            cols = st.columns(3)


            for index, row in recommendations.iterrows():

                movie_title = row["Movie"]

                # Get TMDB information
                tmdb_movie = get_tmdb_movie(
                    movie_title
                )


                with cols[index % 3]:

                    # Start card
                    st.markdown(
                        '<div class="movie-card">',
                        unsafe_allow_html=True
                    )


                    # ==================================================
                    # POSTER
                    # ==================================================

                    if tmdb_movie:

                        poster_url = tmdb_movie.get(
                            "poster_url"
                        )

                        if poster_url:

                            st.image(
                                poster_url,
                                use_container_width=True
                            )

                        else:

                            st.info(
                                "🎬 Poster unavailable"
                            )

                    else:

                        st.info(
                            "🎬 Movie poster unavailable"
                        )


                    # ==================================================
                    # TITLE
                    # ==================================================

                    st.markdown(
                        f'<div class="movie-title">'
                        f'🎬 {movie_title}'
                        f'</div>',
                        unsafe_allow_html=True
                    )


                    # ==================================================
                    # GENRE
                    # ==================================================

                    if "Genre" in row.index:

                        genre = row["Genre"]

                        st.caption(
                            f"🎭 {genre}"
                        )


                    # ==================================================
                    # RATINGS
                    # ==================================================

                    rating_col1, rating_col2 = st.columns(2)


                    # Predicted rating
                    with rating_col1:

                        predicted_rating = row[
                            "Predicted Rating"
                        ]

                        st.metric(
                            "🤖 Predicted",
                            f"{predicted_rating:.2f}/5"
                        )


                    # TMDB rating
                    with rating_col2:

                        if tmdb_movie:

                            tmdb_rating = (
                                tmdb_movie.get("rating")
                            )

                            if tmdb_rating is not None:

                                st.metric(
                                    "⭐ TMDB",
                                    f"{tmdb_rating:.1f}/10"
                                )

                            else:

                                st.metric(
                                    "⭐ TMDB",
                                    "N/A"
                                )

                        else:

                            st.metric(
                                "⭐ TMDB",
                                "N/A"
                            )


                    # ==================================================
                    # RELEASE DATE
                    # ==================================================

                    if tmdb_movie:

                        release_date = (
                            tmdb_movie.get(
                                "release_date"
                            )
                        )

                        if release_date:

                            # Show only year
                            year = release_date[:4]

                            st.caption(
                                f"📅 {year}"
                            )


                    # ==================================================
                    # DESCRIPTION
                    # ==================================================

                    if tmdb_movie:

                        overview = (
                            tmdb_movie.get(
                                "overview"
                            )
                        )

                        if overview:

                            if len(overview) > 170:

                                short_overview = (
                                    overview[:170]
                                    + "..."
                                )

                            else:

                                short_overview = overview


                            st.write(
                                short_overview
                            )

                        else:

                            st.caption(
                                "No description available."
                            )


                    # ==================================================
                    # RECOMMENDATION BADGE
                    # ==================================================

                    st.markdown(
                        '<div class="recommendation-badge">'
                        '👥 Recommended from similar users'
                        '</div>',
                        unsafe_allow_html=True
                    )


                    # Close card
                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


# ==========================================================
# TAB 2 - SIMILAR USERS
# ==========================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        '👥 Similar Users'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Users whose movie-rating patterns are similar "
        "to the selected user."
    )


    try:

        similar_users = (
            recommender.get_similar_users(
                user_id
            )
        )


        if isinstance(
            similar_users,
            pd.DataFrame
        ):

            st.dataframe(
                similar_users,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.write(
                similar_users
            )


    except Exception:

        st.info(
            "Similar user information is not available "
            "from the current recommender."
        )


# ==========================================================
# TAB 3 - RATING HISTORY
# ==========================================================

with tab3:

    st.markdown(
        '<div class="section-title">'
        '⭐ Your Rating History'
        '</div>',
        unsafe_allow_html=True
    )


    try:

        user_history = recommender.ratings[
            recommender.ratings["userId"] == user_id
        ]


        if not user_history.empty:

            st.dataframe(
                user_history,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No rating history found for this user."
            )


    except Exception:

        st.info(
            "Rating history is not available."
        )


# ==========================================================
# TAB 4 - ANALYTICS
# ==========================================================

with tab4:

    st.markdown(
        '<div class="section-title">'
        '📊 Dataset Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    try:

        ratings_data = recommender.ratings


        # --------------------------------------------------
        # DATASET STATISTICS
        # --------------------------------------------------

        total_ratings = len(
            ratings_data
        )

        total_users = (
            ratings_data["userId"]
            .nunique()
        )

        total_movies = (
            ratings_data["movieId"]
            .nunique()
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "⭐ Total Ratings",
                f"{total_ratings:,}"
            )


        with col2:

            st.metric(
                "👥 Users",
                total_users
            )


        with col3:

            st.metric(
                "🎬 Movies",
                total_movies
            )


        st.divider()


        # --------------------------------------------------
        # RATING DISTRIBUTION
        # --------------------------------------------------

        st.subheader(
            "📈 Rating Distribution"
        )


        rating_counts = (
            ratings_data["rating"]
            .value_counts()
            .sort_index()
        )


        fig, ax = plt.subplots(
            figsize=(8, 4)
        )


        ax.bar(
            rating_counts.index,
            rating_counts.values
        )


        ax.set_xlabel(
            "Rating"
        )

        ax.set_ylabel(
            "Number of Ratings"
        )

        ax.set_title(
            "Movie Rating Distribution"
        )


        st.pyplot(
            fig,
            clear_figure=True
        )


    except Exception as e:

        st.warning(
            f"Analytics unavailable: {e}"
        )


# ==========================================================
# MOVIE SEARCH
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🔎 Explore Movies'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Search movies available in the MovieLens dataset."
)


search_text = st.text_input(
    "Search for a movie",
    placeholder="Try: Toy Story, Star Wars, Batman..."
)


if search_text:

    try:

        search_results = (
            recommender.search_movies(
                search_text
            )
        )


        if search_results.empty:

            st.warning(
                "No matching movies found."
            )

        else:

            st.dataframe(
                search_results,
                use_container_width=True,
                hide_index=True
            )


    except Exception:

        st.info(
            "Movie search is not available "
            "from the current recommender."
        )


# ==========================================================
# HOW IT WORKS
# ==========================================================

st.divider()


with st.expander(
    "🧠 How does CineMatch work?"
):

    st.markdown(
        """
### Recommendation Process

**1. User-Movie Matrix**

The system creates a matrix containing
users, movies and their ratings.

**2. User Similarity**

Cosine Similarity compares users based on
their movie-rating patterns.

**3. Similar Users**

The system identifies users with preferences
similar to the selected user.

**4. Rating Prediction**

Ratings from similar users are used to
estimate how much the selected user may
like an unseen movie.

**5. Recommendation**

Movies with the highest predicted ratings
are recommended to the user.

**6. TMDB Integration**

TMDB provides additional movie information
such as posters, descriptions, release dates
and TMDB ratings.
"""
    )


# ==========================================================
# ABOUT PROJECT
# ==========================================================

with st.expander(
    "ℹ️ About This Project"
):

    st.markdown(
        """
### 🎬 CineMatch

A personalized movie recommendation system
built using **User-Based Collaborative Filtering**.

**Machine Learning Technique:**  
User-Based Collaborative Filtering

**Similarity Metric:**  
Cosine Similarity

**Dataset:**  
MovieLens 100K

**Frontend:**  
Streamlit

**Programming Language:**  
Python

**Movie Information:**  
TMDB API
"""
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    '<div class="footer">'
    '🎬 CineMatch | MovieLens 100K | '
    'User-Based Collaborative Filtering | '
    'Cosine Similarity'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Movie data and images provided by TMDB. "
    "This product uses the TMDB API but is not "
    "endorsed or certified by TMDB."
)