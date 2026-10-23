import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("TMDB_API_KEY")

if key:
    print("TMDB key found!")
    print("Key length:", len(key))
    print("First 5 characters:", key[:5])
else:
    print("TMDB key NOT found!")