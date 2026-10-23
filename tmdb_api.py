import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def search_movie(movie_title):
    if not TMDB_API_KEY:
        print("ERROR: TMDB_API_KEY not found.")
        return None

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
        "language": "en-US",
        "include_adult": False
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            return None

        # Prefer a search result that has a poster.
        movie = next(
            (item for item in results if item.get("poster_path")),
            results[0]
        )

        poster_path = movie.get("poster_path")

        return {
            "tmdb_id": movie.get("id"),
            "title": movie.get("title", movie_title),
            "overview": movie.get("overview") or "No overview available.",
            "release_date": movie.get("release_date") or "Unknown",
            "rating": movie.get("vote_average", 0),
            "poster_url": (
                f"{IMAGE_BASE_URL}{poster_path}"
                if poster_path else None
            )
        }

    except requests.exceptions.RequestException as e:
        print(f"TMDB request error: {e}")
        return None

