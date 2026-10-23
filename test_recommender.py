from recommender import MovieRecommender


print("Loading recommendation system...")

recommender = MovieRecommender()

print("Recommendation system loaded!")

print("\nTop Recommendations:")

recommendations = recommender.get_recommendations(
    user_id=1,
    n=10
)

print(recommendations)

print("\nSimilar Users:")

print(
    recommender.get_similar_users(
        user_id=1,
        n=5
    )
)

print("\nUser Statistics:")

print(
    recommender.get_user_stats(
        user_id=1
    )
)