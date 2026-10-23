import pandas as pd

# Load ratings dataset
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

# Create User-Movie Matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)

# Display information
print("USER-MOVIE MATRIX")
print("-----------------")

print("Number of users:", user_movie_matrix.shape[0])
print("Number of movies:", user_movie_matrix.shape[1])

print("\nMatrix shape:")
print(user_movie_matrix.shape)

print("\nFirst 5 users:")
print(user_movie_matrix.head())