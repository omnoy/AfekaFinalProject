from app.models.generatedpost import GeneratedPost
from app.models.social_media import SocialMedia
from typing import Optional
from abc import ABC, abstractmethod

class GeneratedPostService(ABC):

    @abstractmethod
    def __init__(self) -> None:
        "Initialize Generated Posts Database"
        pass   
    
    @abstractmethod
    def generate_post(self, generation_prompt: str, public_official_id: str, 
                      user_id: Optional[str] = None, social_media: Optional[SocialMedia] = None) -> GeneratedPost:
        "Create a Generated Post using a prompt"
        pass
    
    @abstractmethod
    def get_generated_post_by_id(self, post_id: str) -> GeneratedPost:
        "Get a specific generated post by its ObjectID"
        pass

    @abstractmethod
    def get_generated_posts_by_user_id(self, user_id: str) -> list[GeneratedPost]:
        "Get Generated Posts by User ID of creator"
        pass

    @abstractmethod
    def get_all_generated_posts(self) -> list[GeneratedPost]:
        "Get all generated posts from the database"
        pass

    @abstractmethod
    def delete_all_generated_posts(self) -> None:
        "Delete all generated posts from the database"
        pass