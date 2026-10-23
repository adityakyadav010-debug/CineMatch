CineMatch 🎬

CineMatch is a movie recommendation system I built using Python, machine learning, React, and FastAPI. The idea behind this project was simple: recommend movies to users based on their rating history and make it easy to explore and save movies they want to watch later.

I started with the MovieLens 100K dataset and initially built the project using Streamlit. As the project grew, I decided to switch to React for the frontend and FastAPI for the backend. This gave me more flexibility with the UI and made it easier to keep the recommendation logic separate from the frontend.

I also integrated the TMDB API to display movie posters, descriptions, and release dates, and used Supabase to store movies added to the Watchlist.

The project is still running locally, and there are a few things I want to improve before deploying it.

Features
Get movie recommendations based on user ratings.
View movie posters, descriptions, and release dates.
Search for movies by title and filter them by genre.
Add movies to a Watchlist and remove them when needed.
Store Watchlist data in Supabase.
Browse recommendations through a React-based interface.
Tech Stack
Part	Technologies
Frontend	React, Vite, JavaScript, CSS
Backend	Python, FastAPI
Machine Learning	Collaborative Filtering, Pandas, NumPy, Scikit-learn
Database	Supabase (PostgreSQL)
Movie Details	TMDB API
Dataset	MovieLens 100K
How It Works

CineMatch uses the MovieLens 100K dataset, which contains movie ratings from different users.

The recommendation system uses collaborative filtering to find patterns in how users rate movies. Based on these patterns, it estimates which movies a particular user might enjoy.

Users can select a MovieLens user ID to get recommendations. The FastAPI backend handles the recommendation logic and sends the results to the React frontend.

For movie details, I use the TMDB API to fetch information such as posters, descriptions, and release dates. The Watchlist feature is connected to Supabase, so saved movies can be stored and retrieved later.

Project Structure
movieRecommendation/
├── backend/
│   ├── main.py
│   └── supabase_client.py
├── database/
│   └── schema.sql
├── data/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── services/
│   │       └── api.js
│   └── package.json
├── app.py
├── recommender.py
├── recommendations.py
├── similarity.py
├── similar_users.py
├── user_movie_matrix.py
├── tmdb_api.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

Getting Started

Follow these steps to run CineMatch on your local machine.

Prerequisites

Make sure you have the following installed:

Python
Node.js and npm
A TMDB API key
A Supabase project
1. Clone the repository
git clone https://github.com/adityakyadav010-debug/CineMatch.git
cd CineMatch

2. Set up the backend

Create a virtual environment:

python -m venv venv


Activate it on Windows PowerShell:

.\venv\Scripts\Activate.ps1


Install the required Python packages:

python -m pip install -r requirements.txt

3. Configure environment variables

Create a .env file in the project root and add your API credentials:

4. Set up the database

Create a project in Supabase and open its SQL Editor.

Run the SQL script from:

database/schema.sql


This sets up the table used to store Watchlist entries.

At the moment, CineMatch uses MovieLens user IDs rather than individual user accounts. Authentication and separate personal Watchlists are planned improvements.

5. Start the backend

From the project root, run:

python -m uvicorn backend.main:app --reload


The backend should now be available at:

http://127.0.0.1:8000

You can also open the FastAPI documentation to check the available endpoints:

http://127.0.0.1:8000/docs

6. Start the frontend

Open a new terminal and navigate to the frontend folder:

cd frontend
npm install
npm run dev


Open the local URL displayed in your terminal. By default, Vite usually uses:

http://localhost:5173

Make sure the backend is running while using the frontend.

API Endpoints

These are the main endpoints used by the application:

Method	Endpoint	Purpose
GET	/api/users/{user_id}/recommendations?n=10	Get recommendations for a user
GET	/api/watchlist/{user_id}	Retrieve a user's Watchlist
POST	/api/watchlist	Add a movie to the Watchlist
DELETE	/api/watchlist/{user_id}/{movie_id}	Remove a movie from the Watchlist
Challenges and What I Learned

One of the main challenges was getting the different parts of the application to work together.

I started with Streamlit, but eventually moved to React and FastAPI because I wanted more control over the frontend and a separate backend for the recommendation system. That meant adjusting how the frontend communicated with the backend and making sure the API returned the data the UI needed.

I also ran into issues with missing movie posters, Python dependencies, and the Watchlist API. Working through these problems helped me understand more about API integration, frontend-backend communication, and handling data from different sources.

The recommendation system was an important part of the project, but connecting it to a usable interface was just as much of the work.

CineMatch currently works locally, and I still have improvements to make before putting it online.

What's Next?

Here are a few things I want to work on next:

Add login and individual user accounts.
Combine collaborative filtering with content-based recommendations.
Improve movie search and genre filtering.
Make the UI more responsive on mobile devices.
Add automated tests for the backend and recommendation logic.
Deploy the application and improve API and Watchlist security.
Dataset and Credits

MovieLens 100K

The rating data used for the recommendation system comes from GroupLens Research.

Dataset: https://grouplens.org/datasets/movielens/100k/

TMDB

Movie posters and additional movie information are fetched using the TMDB API.

Website: https://www.themoviedb.org/

This product uses the TMDB API but is not endorsed or certified by TMDB.

Author

Aditya Yadav
B.Tech CSE, ABES Engineering College