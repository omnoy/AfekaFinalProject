from typing import Tuple
import re
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.models.language import Language
import logging
from app.generation_model.base_claude_model import BaseClaudeModel

class ClaudeGenerationModel(BaseClaudeModel):
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: SocialMedia) -> str:
        
        prompt_template = ClaudeGenerationModel._get_prompt_template("generation_prompt")
        # prompt template for the llm, where the variables will be inserted when invoked
        
        llm = ClaudeGenerationModel.get_claude_model(stop_sequences=["[GENERATION_SUCCESSFUL]", "[GENERATION_FAILED]"])
        # claude llm model that generates the response  
        
        chain = (
            prompt_template # prompt template for llm
            | llm # llm model that generates a response
            | ClaudeGenerationModel._validate_response #validates that response was successful
            | ClaudeGenerationModel._extract_from_response #extracts title and text from response
        )
        
        prompt_info_dict = ClaudeGenerationModel._create_prompt_info_dict(generation_prompt, public_official, language, social_media)
        
        response = chain.invoke(prompt_info_dict)
        
        return response["title"], response["text"]
    
    @staticmethod
    def _validate_response(response) -> Tuple[str]:
        
        logging.info(f"Generation Model Anthropic API response: {response}")
        
        if response.response_metadata["stop_reason"] != "stop_sequence":
            raise PostGenerationFailureException("No Stop Sequence Found in Generation Response")
        elif response.response_metadata["stop_sequence"] != "[GENERATION_SUCCESSFUL]":
            raise PostGenerationFailureException("Invalid Prompt")

        return response

    @staticmethod
    def _extract_from_response(response):
        post_title = ClaudeGenerationModel._extract_from_annotation(response.content, "title")

        post_text = ClaudeGenerationModel._extract_from_annotation(response.content, "content")

        return {"title": post_title, "text": post_text}

    @staticmethod
    def _extract_from_annotation(text: str, annotation: str=""):
        pattern = r"<" + re.escape(annotation) + r">(.*?)</" + re.escape(annotation) + r">"
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None
    
    @staticmethod
    def _create_prompt_info_dict(generation_prompt: str, public_official: PublicOfficial, language: Language, social_media: SocialMedia) -> str:
        public_official_name = public_official.full_name[str(language)]
        public_official_information = ""
        if public_official.age is not None:
            public_official_information += f"{public_official_name} is {public_official.age} years old."
        if public_official.political_party is not None:
            public_official_information += f"{public_official_name} belongs to the {public_official.political_party[str(language)]} political party."
        
        prompt_info_dict = {
                "SOCIAL_MEDIA": str(social_media),
                "PUBLIC_OFFICIAL_NAME": public_official_name,
                "PUBLIC_OFFICIAL_ROLE": public_official.position[str(language)],
                "PUBLIC_OFFICIAL_INFORMATION": public_official_information,
                "LANGUAGE": language.get_full_name(),
                "input": generation_prompt
        }

        return prompt_info_dict