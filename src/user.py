from flask_login import UserMixin
from src.supabase import Supabase

class User(UserMixin):

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
    
    @staticmethod
    def get(user_id):
        db = Supabase.getSupabaseClient()
        user = db.table("Users").select("*").eq("id", user_id).execute().data[0]
        if not user:
            return None
        user = User(id_=user[0], name=user[1], email=user[2], picture=user[3])
        return user
    
    @staticmethod
    def create(id, name, email, picture):
        db = Supabase.getSupabaseClient()
        db.table("Users").insert({"id": id, "name": name, "email": email, "picture": picture}).execute()
