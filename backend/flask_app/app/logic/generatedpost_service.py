from app.models.generatedpost import GeneratedPost
from app.models.generationprompt import GenerationPrompt
class GeneratedPostService:
    
    def __init__(self) -> None:
        "Initialize Generated Posts Database"
        pass   

    def generate_post(self, generation_prompt: GenerationPrompt) -> GeneratedPost:
        "Create a User for the Database using prompt"
        pass
    
    def get_generated_post_by_id(self, post_id: str) -> GeneratedPost:
        "Get a specific generated post by its ObjectID"
        pass

    def get_generated_posts_by_user_id(self, user_id: str) -> list[GeneratedPost]:
        "Get Generated Posts by user ID of creator"
        pass

    def get_generated_posts_by_public_official_id(self, po_id: str) -> list[GeneratedPost]:
        "Get Generated Posts by public official ID"
        pass

    def get_all_generated_posts(self) -> list[GeneratedPost]:
        "Get all generated posts from the database"
        pass

    def delete_all_generated_posts(self) -> None:
        "Delete all generated posts from the database"
        pass