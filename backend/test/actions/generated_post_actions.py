from app.logic.mongo.database import get_generated_post_collection
from app.models.generatedpost import GeneratedPost

class GeneratedPostActions():
    def __init__(self, client):
        self.client = client

    def create_generated_post(self, user_id: str, public_official_id: str, title="Title", text="Text", prompt="Prompt", social_media="facebook") -> GeneratedPost:
        generated_post_dict = {
            "user_id": user_id, 
            "public_official_id": public_official_id, 
            "title": title, 
            "text": text, 
            "prompt": prompt, 
            "language": "heb",
            "social_media": social_media
        }

        inserted_obj = get_generated_post_collection().insert_one(generated_post_dict)
        generated_post_dict["_id"] = inserted_obj.inserted_id
        self.generated_post = GeneratedPost(**generated_post_dict)
        return self.generated_post
    
    def get_generated_post_id(self) -> str:
        return self.generated_post.get_id()