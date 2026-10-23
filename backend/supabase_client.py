
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

# Locate the project's root directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Load environment variables
load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate configuration
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in .env")

# Reusable Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
