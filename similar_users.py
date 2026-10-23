import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


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



user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)



similarity_matrix = cosine_similarity(
    user_movie_matrix
)


user_similarity = pd.DataFrame(
    similarity_matrix,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)


user_id = 1


similar_users = (
    user_similarity[user_id]
    .sort_values(
        ascending=False
    )
)


# Remove the selected user
similar_users = similar_users[
    similar_users.index != user_id
]


# Select top 10 similar users
top_similar_users = similar_users.head(10)



print("TOP 10 USERS SIMILAR TO USER", user_id)
print("--------------------------------------")

for other_user, similarity in top_similar_users.items():

    print(
        f"User {other_user} "
        f"→ Similarity: {similarity:.4f}"
    )