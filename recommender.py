import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self):

        # ==========================================
        # LOAD RATINGS
        # ==========================================

        self.ratings = pd.read_csv(
            "data/ml-100k/u.data",
            sep="\t",
            names=[
                "userId",
                "movieId",
                "rating",
                "timestamp"
            ]
        )

        # ==========================================
        # LOAD MOVIES
        # ==========================================

        movie_columns = [
            "movieId",
            "title",
            "release_date",
            "video_release_date",
            "IMDb_URL",
            "unknown",
            "Action",
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western"
        ]

        self.movies = pd.read_csv(
            "data/ml-100k/u.item",
            sep="|",
            encoding="latin-1",
            header=None,
            names=movie_columns
        )

        # ==========================================
        # CREATE GENRE COLUMN
        # ==========================================

        genre_columns = [
            "unknown",
            "Action",
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western"
        ]

        self.movies["genres"] = self.movies[
            genre_columns
        ].apply(
            lambda row: ", ".join(
                [
                    genre
                    for genre in genre_columns
                    if row[genre] == 1
                ]
            ),
            axis=1
        )

        # ==========================================
        # USER-MOVIE MATRIX
        # ==========================================

        self.user_movie_matrix = (
            self.ratings
            .pivot_table(
                index="userId",
                columns="movieId",
                values="rating"
            )
            .fillna(0)
        )

        # ==========================================
        # USER SIMILARITY
        # ==========================================

        similarity_matrix = cosine_similarity(
            self.user_movie_matrix
        )

        self.user_similarity = pd.DataFrame(
            similarity_matrix,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index
        )

    # =================================================
    # RECOMMEND MOVIES
    # =================================================

    def get_recommendations(
        self,
        user_id,
        n=10
    ):

        if user_id not in self.user_similarity.index:
            return pd.DataFrame()

        # Find similar users
        similar_users = (
            self.user_similarity[user_id]
            .sort_values(
                ascending=False
            )
        )

        # Remove selected user
        similar_users = similar_users[
            similar_users.index != user_id
        ]

        # Select top similar users
        top_users = similar_users.head(10)

        # Movies already rated by user
        watched_movies = set(
            self.ratings[
                self.ratings["userId"] == user_id
            ]["movieId"]
        )

        recommendations = []

        # Calculate prediction for every unseen movie
        for movie_id in self.movies["movieId"]:

            if movie_id in watched_movies:
                continue

            movie_ratings = self.ratings[
                self.ratings["movieId"] == movie_id
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
                        "Predicted Rating": round(
                            predicted_rating,
                            2
                        )
                    }
                )

        recommendations = pd.DataFrame(
            recommendations
        )

        if recommendations.empty:
            return recommendations

        # Sort
        recommendations = (
            recommendations
            .sort_values(
                "Predicted Rating",
                ascending=False
            )
            .head(n)
        )

        # Add movie details
        recommendations = recommendations.merge(
            self.movies[
                [
                    "movieId",
                    "title",
                    "genres"
                ]
            ],
            on="movieId"
        )

        recommendations = recommendations.rename(
            columns={
                "title": "Movie",
                "genres": "Genre"
            }
        )

        return recommendations[
            [
                "Movie",
                "Genre",
                "Predicted Rating"
            ]
        ]

    # =================================================
    # SIMILAR USERS
    # =================================================

    def get_similar_users(
        self,
        user_id,
        n=5
    ):

        if user_id not in self.user_similarity.index:
            return pd.DataFrame()

        similar_users = (
            self.user_similarity[user_id]
            .sort_values(
                ascending=False
            )
        )

        similar_users = similar_users[
            similar_users.index != user_id
        ]

        result = (
            similar_users
            .head(n)
            .reset_index()
        )

        result.columns = [
            "User ID",
            "Similarity"
        ]

        result["Similarity"] = (
            result["Similarity"]
            .round(3)
        )

        return result

    # =================================================
    # USER HISTORY
    # =================================================

    def get_user_history(
        self,
        user_id
    ):

        history = self.ratings[
            self.ratings["userId"] == user_id
        ].merge(
            self.movies[
                [
                    "movieId",
                    "title",
                    "genres"
                ]
            ],
            on="movieId"
        )

        history = history.sort_values(
            "rating",
            ascending=False
        )

        history = history.rename(
            columns={
                "title": "Movie",
                "genres": "Genre",
                "rating": "Rating"
            }
        )

        return history[
            [
                "Movie",
                "Genre",
                "Rating"
            ]
        ]


    def get_user_stats(
        self,
        user_id
    ):

        user_ratings = self.ratings[
            self.ratings["userId"] == user_id
        ]

        return {
            "movies_rated": len(
                user_ratings
            ),
            "average_rating": round(
                user_ratings["rating"].mean(),
                2
            )
        }

    # =================================================
    # SEARCH MOVIES
    # =================================================

    def search_movies(
        self,
        search_text
    ):

        results = self.movies[
            self.movies["title"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        return results[
            [
                "title",
                "genres"
            ]
        ].rename(
            columns={
                "title": "Movie",
                "genres": "Genre"
            }
        )