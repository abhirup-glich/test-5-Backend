import os
from supabase import create_client, Client
from ..config import Config

def get_supabase_client() -> Client:
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_KEY
    if not url or not key:
        # Fallback or error if env vars not set, but allow import for testing
        return None
    return create_client(url, key)

supabase: Client = get_supabase_client()
