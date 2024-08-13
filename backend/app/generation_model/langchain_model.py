from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.generation_model.post_generation_model import PostGenerationModel
from app.generation_model.claude_generation_model import ClaudeGenerationModel
from app.models.language import Language
from app.generation_model.prompt_injection_detection_model import PromptInjectionDetectionModel
import logging

class LangChainModel(PostGenerationModel):
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: SocialMedia) -> str:
        
        #TODO prompt injection prevention
        if PromptInjectionDetectionModel.detect_prompt_injection(generation_prompt):
            logging.error("Prompt injection detected")
            raise ValueError("Prompt injection detected")
        
        post_title, post_text = ClaudeGenerationModel.generate_post(generation_prompt, public_official, language, social_media)
        logging.info(f"Generated post title: {post_title}, text: {post_text}")
        
        return post_title, post_text