from tmdb_api import search_movie


movie = search_movie("Toy Story")

if movie:

    print("TMDB API working!")
    print("Title:", movie["title"])
    print("Release:", movie["release_date"])
    print("Rating:", movie["rating"])
    print("Poster:", movie["poster_url"])

else:

    print("Movie not found.")