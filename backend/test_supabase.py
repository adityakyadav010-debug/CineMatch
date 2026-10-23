
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

# Find the .env file in the project root
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

# Read Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing in .env")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Supabase client initialized!")

try:
    # Read only: do not insert or delete any data
    response = (
        supabase.table("watchlist")
        .select("id")
        .limit(1)
        .execute()
    )

    print("Database connection successful!")
    print("Watchlist query completed successfully.")

except Exception as error:
    print("Database connection failed!")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
