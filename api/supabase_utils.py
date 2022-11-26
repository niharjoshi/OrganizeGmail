import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class SupabaseUtils:

    def __init__(self):
        self.SUPABASE_URL = os.environ.get("SUPABASE_URL")
        self.SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
        self.supabase_client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
    
    def getSupabaseClient(self):
        return self.supabase_client
