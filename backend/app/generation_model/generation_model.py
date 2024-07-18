from abc import ABC, abstractmethod
from typing import Optional
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.models.language import Language

class GenerationModel(ABC):

    @abstractmethod
    def __init__(self):
        "Initialize Generation Model"
        pass

    @abstractmethod
    def generate_post(self, generation_prompt: str, public_official: PublicOfficial, language: Language, social_media: Optional[SocialMedia]) -> str:
        "Generate a social media post according to a prompt"
        pass

    @abstractmethod
    def get_model_type(self) -> str:
        "Get the name of the model"
        pass