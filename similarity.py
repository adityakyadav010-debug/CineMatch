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

print("USER SIMILARITY MATRIX")
print("----------------------")

print(
    "Matrix shape:",
    user_similarity.shape
)


user_id = 1

similar_users = (
    user_similarity[user_id]
    .sort_values(ascending=False)
)


print("\nSimilarity with User 1:")
print(similar_users.head(10))