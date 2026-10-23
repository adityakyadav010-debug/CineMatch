import streamlit as st
import matplotlib.pyplot as plt

from recommender import MovieRecommender


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ==========================================================
# LOAD RECOMMENDER
# ==========================================================

@st.cache_resource
def load_recommender():

    return MovieRecommender()


with st.spinner("Loading recommendation system..."):

    recommender = load_recommender()


# ==========================================================
# TITLE
# ==========================================================

st.title(
    "🎬 Personalized Movie Recommendation System"
)

st.write(
    "A movie recommendation system using "
    "User-Based Collaborative Filtering "
    "and Cosine Similarity."
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header(
    "⚙️ Recommendation Settings"
)

user_id = st.sidebar.selectbox(
    "Select User",
    recommender.user_movie_matrix.index.tolist()
)

number_of_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    5,
    15,
    10
)


# ==========================================================
# USER STATISTICS
# ==========================================================

stats = recommender.get_user_stats(
    user_id
)

st.subheader("👤 User Profile")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "User ID",
        user_id
    )

with col2:

    st.metric(
        "Movies Rated",
        stats["movies_rated"]
    )

with col3:

    st.metric(
        "Average Rating",
        stats["average_rating"]
    )


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.divider()

st.header(
    "🎯 Personalized Recommendations"
)

if st.button(
    "✨ Generate Recommendations",
    use_container_width=True
):

    with st.spinner(
        "Finding movies you may like..."
    ):

        recommendations = (
            recommender
            .get_recommendations(
                user_id,
                number_of_recommendations
            )
        )

    if recommendations.empty:

        st.warning(
            "No recommendations found."
        )

    else:

        st.success(
            "Recommendations generated!"
        )

        st.dataframe(
            recommendations,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# SIMILAR USERS
# ==========================================================

st.divider()

st.header(
    "👥 Users With Similar Preferences"
)

if st.button(
    "🔍 Find Similar Users",
    use_container_width=True
):

    similar_users = (
        recommender
        .get_similar_users(
            user_id,
            5
        )
    )

    st.dataframe(
        similar_users,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# USER HISTORY
# ==========================================================

st.divider()

st.header(
    "⭐ User Rating History"
)

history = recommender.get_user_history(
    user_id
)

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# RATING DISTRIBUTION
# ==========================================================

st.divider()

st.header(
    "📊 Rating Distribution"
)

rating_counts = (
    recommender.ratings[
        "rating"
    ]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots()

ax.bar(
    rating_counts.index,
    rating_counts.values
)

ax.set_xlabel("Rating")

ax.set_ylabel(
    "Number of Ratings"
)

ax.set_title(
    "Movie Rating Distribution"
)

st.pyplot(
    fig
)


# ==========================================================
# MOVIE SEARCH
# ==========================================================

st.divider()

st.header(
    "🔎 Search Movies"
)

search_text = st.text_input(
    "Enter movie name"
)

if search_text:

    search_results = (
        recommender
        .search_movies(
            search_text
        )
    )

    if search_results.empty:

        st.info(
            "No movies found."
        )

    else:

        st.dataframe(
            search_results,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Movie Recommendation System | "
    "MovieLens 100K | "
    "User-Based Collaborative Filtering"
)