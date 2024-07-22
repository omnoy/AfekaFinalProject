from app.models.generatedpost import GeneratedPost
from app.models.social_media import SocialMedia
from abc import ABC, abstractmethod
from app.models.language import Language
from app.models.publicofficial import PublicOfficial
from app.models.user import User

class GeneratedPostService(ABC):

    @abstractmethod
    def __init__(self) -> None:
        "Initialize Generated Posts Database"
        pass   
    
    @abstractmethod
    def generate_post(self, user: User, public_official: PublicOfficial, generation_prompt: str, 
                      language: Language, social_media: SocialMedia) -> GeneratedPost:
        "Create a Generated Post using a prompt"
        pass
    
    @abstractmethod
    def get_generated_post_by_id(self, post_id: str) -> GeneratedPost:
        "Get a specific generated post by its ObjectID"
        pass
    
    @abstractmethod
    def get_generated_post_by_id_list(self, post_id_list: list[str]) -> list[GeneratedPost]:
        "Get a list of generated posts by their ObjectIDs"
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