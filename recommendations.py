import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# =====================================================
# 1. LOAD RATINGS
# =====================================================

ratings = pd.read_csv(
    "data/ml-100k/u.data",
    sep="\t",
    names=[
        "userId",
        "movieId",
        "rating",
        "timestamp"
    ]
)


# =====================================================
# 2. LOAD MOVIE INFORMATION
# =====================================================

movies = pd.read_csv(
    "data/ml-100k/u.item",
    sep="|",
    encoding="latin-1",
    header=None,
    usecols=[0, 1],
    names=[
        "movieId",
        "title"
    ]
)


# =====================================================
# 3. CREATE USER-MOVIE MATRIX
# =====================================================

user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)


# =====================================================
# 4. CALCULATE USER SIMILARITY
# =====================================================

similarity_matrix = cosine_similarity(
    user_movie_matrix
)

user_similarity = pd.DataFrame(
    similarity_matrix,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)


# =====================================================
# 5. SELECT USER
# =====================================================

user_id = 1


# =====================================================
# 6. FIND SIMILAR USERS
# =====================================================

similar_users = (
    user_similarity[user_id]
    .sort_values(ascending=False)
)

# Remove current user
similar_users = similar_users[
    similar_users.index != user_id
]

# Take top 10 similar users
top_users = similar_users.head(10)


# =====================================================
# 7. FIND MOVIES ALREADY RATED BY USER
# =====================================================

watched_movies = set(
    ratings[
        ratings["userId"] == user_id
    ]["movieId"]
)


print("Movies already rated by User", user_id)
print(len(watched_movies))


# =====================================================
# 8. CALCULATE PREDICTED RATINGS
# =====================================================

recommendations = []


for movie_id in movies["movieId"]:

    if movie_id in watched_movies:
        continue

    movie_ratings = ratings[
        ratings["movieId"] == movie_id
    ]

    weighted_sum = 0
    similarity_sum = 0

    for other_user, similarity in top_users.items():

        user_rating = movie_ratings[
            movie_ratings["userId"] == other_user
        ]

        if not user_rating.empty:

            rating = user_rating.iloc[0]["rating"]

            weighted_sum += (
                similarity * rating
            )

            similarity_sum += abs(
                similarity
            )

    if similarity_sum > 0:

        predicted_rating = (
            weighted_sum / similarity_sum
        )

        recommendations.append(
            {
                "movieId": movie_id,
                "predicted_rating": predicted_rating
            }
        )


recommendations = pd.DataFrame(
    recommendations
)


recommendations = recommendations.sort_values(
    "predicted_rating",
    ascending=False
)



top_recommendations = recommendations.head(10)


top_recommendations = top_recommendations.merge(
    movies,
    on="movieId"
)


print("\n")
print("==========================================")
print(" PERSONALIZED MOVIE RECOMMENDATIONS")
print("==========================================")

for index, row in top_recommendations.iterrows():

    print(
        f"{row['title']} "
        f"→ Predicted Rating: "
        f"{row['predicted_rating']:.2f}"
    )