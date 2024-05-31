from typing import Optional
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.generation_model.generation_model import GenerationModel

class ClaudeModel(GenerationModel):
    
    def __init__(self):
        # TODO fill this later
        pass
    
    def generate_post(self, generation_prompt: str, public_official: PublicOfficial,
                        social_media: Optional[SocialMedia]) -> str:
        return "my name jeff"

    def get_model_type(self) -> str:
        return "Claude"