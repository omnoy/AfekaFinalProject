from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.generation_model.post_generation_model import PostGenerationModel
from app.generation_model.claude_generation_model import ClaudeGenerationModel
from app.generation_model.claude_validation_model import ClaudeValidationModel
from app.models.language import Language
import logging
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException

class GenerationModelWrapper(PostGenerationModel):
    
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: SocialMedia) -> str:
        post_title, post_text = ClaudeGenerationModel.generate_post(generation_prompt, public_official, language, social_media)
        logging.info(f"Generated post title: {post_title}, text: {post_text}")
        
        validation_results = ClaudeValidationModel.validate_post(post_title, post_text)
        logging.info(f"Validation results: {validation_results}")
        
        if validation_results["valid"] == "true":
            return post_title, post_text
        else:
            raise PostGenerationFailureException(f"Reason: {validation_results['reason']}")
        