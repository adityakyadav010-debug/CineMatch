
-- CineMatch Supabase Database Schema
-- Creates the Watchlist table for MovieLens user profiles

CREATE TABLE IF NOT EXISTS public.watchlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id INTEGER NOT NULL
        CHECK (user_id BETWEEN 1 AND 943),

    movie_title TEXT NOT NULL,

    genre TEXT,
    poster_url TEXT,
    overview TEXT,
    release_date TEXT,
    predicted_rating DOUBLE PRECISION,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (user_id, movie_title)
);

-- Index for faster Watchlist queries
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id
ON public.watchlist (user_id);

-- Enable Row Level Security
ALTER TABLE public.watchlist
ENABLE ROW LEVEL SECURITY;
