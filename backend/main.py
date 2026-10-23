from backend.supabase_client import supabase
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from recommender import MovieRecommender
from tmdb_api import search_movie

app = FastAPI(title="Movie Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load existing ML recommender once
recommender = MovieRecommender()


@app.get("/")
def home():
    return {"message": "Movie Recommendation Backend is Running!"}


@app.get("/api/health")
def health():
    return {"status": "success"}


@app.get("/api/users")
def get_users():
    return {
        "users": [
            int(user_id)
            for user_id in recommender.user_movie_matrix.index
        ]
    }


def validate_user(user_id):
    if user_id not in recommender.user_similarity.index:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


@app.get("/api/users/{user_id}/recommendations")
def get_recommendations(
    user_id: int,
    n: int = Query(default=10, ge=1, le=50)
):
    validate_user(user_id)

    results = recommender.get_recommendations(user_id, n)

    return {
        "user_id": user_id,
        "recommendations": results.to_dict(orient="records")
    }


@app.get("/api/users/{user_id}/similar")
def get_similar_users(user_id: int):
    validate_user(user_id)

    results = recommender.get_similar_users(user_id)

    return {
        "similar_users": results.to_dict(orient="records")
    }


@app.get("/api/users/{user_id}/history")
def get_user_history(user_id: int):
    validate_user(user_id)

    results = recommender.get_user_history(user_id)

    return {
        "history": results.to_dict(orient="records")
    }


@app.get("/api/users/{user_id}/stats")
def get_user_stats(user_id: int):
    validate_user(user_id)

    stats = recommender.get_user_stats(user_id)

    return stats


@app.get("/api/movies/search")
def search_movies(q: str = Query(min_length=1)):
    results = recommender.search_movies(q)

    return {
        "movies": results.head(20).to_dict(orient="records")
    }

@app.get("/api/movies/details")
def get_movie_details(title: str):
    movie = search_movie(title)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie details not found on TMDB"
        )

    return movie

class WatchlistMovie(BaseModel):
    user_id: int = Field(ge=1, le=943)
    movie_title: str = Field(min_length=1)
    genre: str | None = None
    poster_url: str | None = None
    overview: str | None = None
    release_date: str | None = None
    predicted_rating: float | None = None


# Fetch saved movies for a MovieLens user
@app.get("/api/watchlist/{user_id}")
def get_user_watchlist(user_id: int):
    
    if not 1 <= user_id <= 943:
        raise HTTPException(
            status_code=400,
            detail="User ID must be between 1 and 943"
        )

    try:
        response = (
            supabase.table("watchlist")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "user_id": user_id,
            "movies": response.data
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve watchlist"
        )

@app.post("/api/watchlist", status_code=201)
def add_to_watchlist(movie: WatchlistMovie):
    try:
        response = (
            supabase.table("watchlist")
            .upsert(
                movie.model_dump(),
                on_conflict="user_id,movie_title"
            )
            .execute()
        )

        return {
            "message": "Movie saved successfully!",
            "movie": response.data[0]
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to save movie to watchlist"
        )

@app.delete("/api/watchlist/{user_id}/{movie_id}")
def delete_watchlist_movie(user_id: int, movie_id: int):

    if not 1 <= user_id <= 943:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    try:
        response = (
            supabase.table("watchlist")
            .delete()
            .eq("user_id", user_id)
            .eq("id", movie_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Movie not found in watchlist"
            )

        return {
            "message": "Movie removed successfully!"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to remove movie"
        )
