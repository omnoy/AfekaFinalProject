from abc import ABC, abstractmethod
from typing import Optional
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.models.language import Language

class PostGenerationModel(ABC):

    @abstractmethod
    def generate_post(self, generation_prompt: str, public_official: PublicOfficial, language: Language, social_media: Optional[SocialMedia]) -> str:
        "Generate a social media post according to a prompt"
        pass