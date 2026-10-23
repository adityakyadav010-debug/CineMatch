# 🎬 CineMatch — Movie Recommendation System

A full-stack movie recommendation web application built using **Machine Learning, React, FastAPI, and Supabase**.

CineMatch provides personalized movie recommendations based on MovieLens user ratings and enriches movie information using the TMDB API.

## Features

- Personalized movie recommendations using machine learning
- Movie posters, descriptions, and release dates from TMDB
- Search movies by title
- Filter movies by genre
- Add and remove movies from a personal Watchlist
- Persistent cloud-based Watchlist using Supabase
- User selection for MovieLens user profiles
- Responsive movie discovery interface

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Machine Learning | Collaborative Filtering, Pandas, NumPy |
| Database | Supabase (PostgreSQL) |
| Movie Information | TMDB API |
| Dataset | MovieLens 100K |

## Project Structure

```text
movieRecommendation/
├── backend/
│   ├── main.py
│   └── supabase_client.py
├── data/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── services/
│   │       └── api.js
│   └── package.json
├── recommender.py
├── tmdb_api.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation and Setup

### Prerequisites

- Python
- Node.js and npm
- Supabase project
- TMDB API key

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CineMatch.git
cd CineMatch
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Python dependencies

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required libraries:

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

```env
TMDB_API_KEY=your_tmdb_api_key
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_key
```

Never commit real API credentials.

### 4. Configure Supabase

Create a Supabase project and a `watchlist` table with the columns required by the backend.

The Watchlist API currently uses MovieLens user IDs for local demonstration. Authentication and authorization must be implemented before public deployment.

### 5. Start the FastAPI backend

From the project root:

```powershell
python -m uvicorn backend.main:app --reload
```

Backend API documentation:

http://127.0.0.1:8000/docs

### 6. Start the React frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local address shown by Vite, typically:

http://localhost:5173

## How It Works

1. A user selects a MovieLens user profile.
2. The recommendation model predicts movie preferences using collaborative filtering.
3. FastAPI returns recommended movie titles and predicted ratings.
4. TMDB enriches recommendations with movie posters and details.
5. React displays recommendations and allows users to save movies.
6. Supabase stores Watchlist records for the selected profile.

## Dataset

This project uses the **MovieLens 100K** dataset for collaborative filtering.

Dataset source: https://grouplens.org/datasets/movielens/100k/

## Future Improvements

- User authentication and secure account-specific Watchlists
- More advanced recommendation algorithms
- Improved recommendation accuracy
- Cloud deployment
- Additional UI/UX enhancements

## Project Status

Core application implemented and tested locally. Public deployment is not yet configured.

## Author

Aditya Yadav

B.Tech — Computer Science and Engineering

ABES Engineering College