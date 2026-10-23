import pandas as pd

# Load ratings
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

# Load movies
movies = pd.read_csv(
    "data/ml-100k/u.item",
    sep="|",
    encoding="latin-1",
    header=None
)

print("First 5 ratings:")
print(ratings.head())

print("\nFirst 5 movies:")
print(movies.iloc[:5, :2])

print("\nDataset Information")
print("-------------------")

print("Total ratings:", len(ratings))
print("Total users:", ratings["userId"].nunique())
print("Total movies:", ratings["movieId"].nunique())