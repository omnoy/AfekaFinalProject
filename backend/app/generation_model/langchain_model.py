from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.generation_model.post_generation_model import PostGenerationModel
from app.generation_model.claude_generation_model import ClaudeGenerationModel
from app.models.language import Language
import logging

class LangChainModel(PostGenerationModel):
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: SocialMedia) -> str:
        
        #TODO prompt injection prevention
        post_title, post_text = ClaudeGenerationModel.generate_post(generation_prompt, public_official, language, social_media)
        logging.info(f"Generated post title: {post_title}, text: {post_text}")
        
        return post_title, post_text