from flask_login import UserMixin
from supabase import Supabase

class User(UserMixin):

    def __init__(self, gid, name, email, picture):
        self.gid = gid
        self.name = name
        self.email = email
        self.picture = picture
    
    def get_id(self):
        return (self.gid)
    
    @staticmethod
    def get(user_id):
        db = Supabase().getSupabaseClient()
        try:
            user = db.table("Users").select("*").eq("gid", user_id).execute().data[0]
        except IndexError:
            return None
        user = User(gid=user["gid"], name=user["name"], email=user["email"], picture=user["picture"])
        return user
    
    @staticmethod
    def create(gid, name, email, picture):
        db = Supabase().getSupabaseClient()
        db.table("Users").insert({"gid": gid, "name": name, "email": email, "picture": picture}).execute()
