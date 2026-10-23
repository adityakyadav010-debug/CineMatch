
const API_BASE_URL = "http://127.0.0.1:8000";

export async function getRecommendations(userId = 1, n = 10) {
  const response = await fetch(
    `${API_BASE_URL}/api/users/${userId}/recommendations?n=${n}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  const data = await response.json();

  return data.recommendations;
}

export async function getMovieDetails(title) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/movies/details?title=${encodeURIComponent(title)}`
  );

  if (!response.ok) {
    return null;
  }

  return await response.json();
}

const WATCHLIST_API = "http://127.0.0.1:8000/api/watchlist";

// Get saved movies for a user
export async function getWatchlist(userId) {
  const response = await fetch(`${WATCHLIST_API}/${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch watchlist");
  }

  return response.json();
}

// Save a movie to Supabase
export async function saveToWatchlist(movie) {
  const response = await fetch(WATCHLIST_API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(movie),
  });

  if (!response.ok) {
    throw new Error("Failed to save movie");
  }

  return response.json();
}

// Delete a movie using its database record ID
export async function removeFromWatchlist(userId, movieId) {
  const response = await fetch(
    `${WATCHLIST_API}/${userId}/${movieId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to remove movie");
  }

  return response.json();
}
