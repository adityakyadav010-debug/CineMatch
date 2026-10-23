
import { useState, useEffect } from "react";
import {
  getRecommendations,
  getMovieDetails,
  getWatchlist,
  saveToWatchlist,
  removeFromWatchlist,
} from "./services/api";
import "./App.css";


function App() {
  const [search, setSearch] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("All");
  const [cloudWatchlist, setCloudWatchlist] = useState([]);
  const [updatingMovie, setUpdatingMovie] = useState(null);
  const [notification, setNotification] = useState("");

  useEffect(() => {
    if (!notification) return;

    const timer = setTimeout(() => {
      setNotification("");
    }, 3000);

    return () => clearTimeout(timer);
  }, [notification]);

  const [showWatchlist, setShowWatchlist] = useState(false);
  const [movies, setMovies] = useState([]);
  const [userId, setUserId] = useState(1);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [postersLoading, setPostersLoading] = useState(false);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadWatchlist() {
      try {
        const data = await getWatchlist(userId);

        setCloudWatchlist(data.movies || []);

        console.log("Supabase Watchlist:", data.movies);
      } catch (error) {
        console.error("Failed to load Supabase Watchlist:", error);
      }
    }

    loadWatchlist();
  }, [userId]);


  useEffect(() => {
    async function loadMovies() {
      try {
        const data = await getRecommendations(userId, 10);


        const formattedMovies = data.map((movie, index) => ({
          id: index,
          title: movie.Movie,
          genre: movie.Genre,
          rating: movie["Predicted Rating"],
          poster: null,
          overview: "",
          releaseDate: "",
        }));

        // Display recommendations immediately
        setMovies(formattedMovies);

        // Fetch posters and movie details
        setPostersLoading(true);
        const moviesWithPosters = await Promise.all(
          formattedMovies.map(async (movie) => {
            try {
              // MovieLens titles often contain a year, e.g. "Toy Story (1995)"
              const cleanTitle = movie.title.replace(/\s*\(\d{4}\)\s*$/, "");

              const details = await getMovieDetails(cleanTitle);

              return {
                ...movie,
                poster: details?.poster_url || null,
                overview: details?.overview || "",
                releaseDate: details?.release_date || "",
              };
            } catch (error) {
              console.error("TMDB error:", movie.title, error);
              return movie;
            }
          })
        );

        setMovies(moviesWithPosters);
        setPostersLoading(false);


      } catch (err) {
        console.error(err);
        setError("Unable to load recommendations. Check FastAPI.");
      } finally {
        setLoading(false);
      }
    }

    setLoading(true);
    setError("");
    loadMovies();
  }, [userId]);


  const watchlistMovies = cloudWatchlist.map((item) => ({
    id: item.id,
    title: item.movie_title,
    genre: item.genre || "Unknown",
    poster: item.poster_url,
    overview: item.overview || "",
    releaseDate: item.release_date || "",
    rating: item.predicted_rating,
  }));

  const displayedMovies = showWatchlist
    ? watchlistMovies
    : movies;


  const genres = [
    "All",
    ...new Set(
      displayedMovies
        .flatMap((movie) => (movie.genre || "").split("|"))
        .map((genre) => genre.trim())
        .filter(Boolean)
    ),
  ].sort((a, b) => {
    if (a === "All") return -1;
    if (b === "All") return 1;
    return a.localeCompare(b);
  });

  const filteredMovies = displayedMovies.filter((movie) => {
    const matchesSearch = movie.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const movieGenres = (movie.genre || "")
      .split("|")
      .map((genre) => genre.trim());

    const matchesGenre =
      selectedGenre === "All" ||
      movieGenres.includes(selectedGenre);

    return matchesSearch && matchesGenre;
  });

  const toggleWatchlist = async (movie) => {
    if (updatingMovie !== null) return;

    setUpdatingMovie(movie.title);

    try {
      const savedMovie = cloudWatchlist.find(
        (item) => item.movie_title === movie.title
      );

      if (savedMovie) {
        await removeFromWatchlist(userId, savedMovie.id);

        console.log("Removed from Supabase:", movie.title);
        setNotification(`Removed "${movie.title}" from Watchlist`);

      } else {
        const movieData = {
          user_id: userId,
          movie_title: movie.title,
          genre: movie.genre || null,
          poster_url: movie.poster || null,
          overview: movie.overview || null,
          release_date: movie.releaseDate || null,
          predicted_rating:
            movie.rating == null ? null : Number(movie.rating),
        };

        await saveToWatchlist(movieData);
        console.log("Saved to Supabase:", movie.title);
        setNotification(`Added "${movie.title}" to Watchlist`);
      }

      const data = await getWatchlist(userId);
      setCloudWatchlist(data.movies || []);
    } catch (error) {
      console.error("Watchlist operation failed:", error);
      alert("Unable to update Watchlist. Check FastAPI.");
    } finally {
      setUpdatingMovie(null);
    }
  };



  return (
    <div className="app">
      {notification && (
        <div className="toast-notification" role="status">
          <span>{notification}</span>
          <button
            type="button"
            onClick={() => setNotification("")}
            aria-label="Dismiss notification"
          >
            ×
          </button>
        </div>
      )}
      <nav className="navbar">
        <h2 className="logo">🎬 CineMatch</h2>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#movies">Discover</a>
          <button
            className="watchlist-nav-btn"
            onClick={() => {
              setShowWatchlist((previous) => !previous);
              document.getElementById("movies")?.scrollIntoView({
                behavior: "smooth",
              });
            }}
          >
            {showWatchlist ? "Discover Movies" : `Watchlist (${cloudWatchlist.length})`}
          </button>
        </div>
      </nav>

      <section className="hero" id="home">
        <span className="eyebrow">AI-POWERED MOVIE DISCOVERY</span>
        <h1>
          Your Next Favorite Movie
          <br />
          <span>Starts Here.</span>
        </h1>
        <p>
          Discover amazing movies and get personalized recommendations
          powered by machine learning.
        </p>

        <a href="#movies" className="explore-btn">
          Explore Movies →
        </a>
      </section>

      <section className="movies-section" id="movies">

        <div className="user-selector">
          <label htmlFor="userId">Choose User:</label>

          <select
            id="userId"
            value={userId}
            onChange={(e) => setUserId(Number(e.target.value))}
          >
            {Array.from({ length: 943 }, (_, i) => i + 1).map((id) => (
              <option key={id} value={id}>
                User {id}
              </option>
            ))}
          </select>

          <span>Personalized recommendations for User {userId}</span>
        </div>

        <div className="section-header">
          <div>
            <span className="eyebrow">DISCOVER</span>
            <h2>{showWatchlist ? "My Watchlist" : "Explore Movies"}</h2>
          </div>

          <input
            type="text"
            placeholder="Search movies..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          <select
            className="genre-filter"
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
          >
            {genres.map((genre) => (
              <option key={genre} value={genre}>
                {genre === "All" ? "All Genres" : genre}
              </option>
            ))}
          </select>
        </div>
        {loading && <p>Loading AI recommendations...</p>}
        {error && <p style={{ color: "#ff6b6b" }}>{error}</p>}
        <div className="movie-grid">

          {showWatchlist && cloudWatchlist.length === 0 && (
            <div className="empty-watchlist">

              {showWatchlist &&
                cloudWatchlist.length > 0 &&
                filteredMovies.length === 0 && (
                  <div className="empty-watchlist">
                    <h2>🔍 No movies found</h2>

                    <p>
                      No saved movies match "{search}".
                      Try searching for another title.
                    </p>

                    <button onClick={() => setSearch("")}>
                      Clear Search
                    </button>
                  </div>
                )}

              <h2>🎬 Your Watchlist is empty</h2>
              <p>
                Start exploring movies and save your favorites
                to watch later.
              </p>

              <button
                onClick={() => {
                  setShowWatchlist(false);
                  setSearch("");
                }}
              >
                Explore Movies
              </button>
            </div>
          )}

          {filteredMovies.map((movie) => (
            <div
              className="movie-card"
              key={movie.id}
              onClick={() => setSelectedMovie(movie)}
            >

              <div className="movie-poster">
                {movie.poster ? (
                  <img
                    src={movie.poster}
                    alt={`${movie.title} poster`}
                    loading="lazy"
                    onError={(e) => {
                      e.currentTarget.style.display = "none";
                      e.currentTarget.parentElement.classList.add("poster-fallback");
                    }}
                  />
                ) : postersLoading ? (
                  <div className="poster-spinner"></div>
                ) : (
                  <span>🎬</span>
                )}
              </div>


              <div className="movie-info">
                <h3>{movie.title}</h3>
                <p>{movie.genre}</p>

                <div className="movie-footer">
                  <span>⭐ {movie.rating}</span>
                  <button
                    disabled={updatingMovie !== null}
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleWatchlist(movie);
                    }}
                  >

                    {updatingMovie === movie.title
                      ? "Updating..."
                      : cloudWatchlist.some(
                        (item) => item.movie_title === movie.title
                      )
                        ? "✓ Saved"
                        : "+ Watchlist"}

                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredMovies.length === 0 && (
          <p className="empty-message">No movies found.</p>
        )}
      </section>

      {selectedMovie && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedMovie(null)}
        >
          <div
            className="movie-modal"
            role="dialog"
            aria-modal="true"
            aria-label={`${selectedMovie.title} details`}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="modal-close"
              onClick={() => setSelectedMovie(null)}
              aria-label="Close movie details"
            >
              ×
            </button>

            {selectedMovie.poster && (
              <img
                className="modal-poster"
                src={selectedMovie.poster}
                alt={`${selectedMovie.title} poster`}
              />
            )}

            <div className="modal-content">
              <h2>{selectedMovie.title}</h2>
              <p>{selectedMovie.genre}</p>
              <p>⭐ Predicted Rating: {selectedMovie.rating}</p>
              <p>Release Date: {selectedMovie.releaseDate || "Unknown"}</p>
              <h3>Overview</h3>
              <p>{selectedMovie.overview || "No overview available."}</p>
            </div>
          </div>
        </div>
      )}

      <footer>© 2026 CineMatch · Powered by Machine Learning</footer>
    </div>
  );
}

export default App;
