import json
from typing import Optional, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import re
from os import getenv
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.models.language import Language
import logging

class ClaudeGenerationModel():
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: SocialMedia) -> str:
        llm = ChatAnthropic(model=getenv("CLAUDE_MODEL_NAME"),
                            max_tokens=4096, 
                            max_retries=3,
                            stop_sequences=["[GENERATION_SUCCESSFUL]", "[GENERATION_FAILED]"])
        
        prompt_template = ClaudeGenerationModel._get_prompt_template()
        
        prompt_info_dict = ClaudeGenerationModel._create_prompt_info_dict(generation_prompt, public_official, language, social_media)
        
        chain = prompt_template | llm
        
        response = chain.invoke(prompt_info_dict)
        
        logging.info(f"Anthropic API response: {response}")

        post_title, post_text = ClaudeGenerationModel._process_response(response)

        return post_title, post_text
    
    @staticmethod
    def _get_prompt_template() -> ChatPromptTemplate:
        prompt_template_dict = json.load(open("./app/generation_model/prompts/generation_prompt.json", "r"))
        
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    prompt_template_dict["system"]
                ),
                (
                    "human", 
                    prompt_template_dict["user"]
                )
            ]
        )
    
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
    
    @staticmethod
    def _process_response(response) -> Tuple[str]:
        if response.response_metadata["stop_reason"] != "stop_sequence":
            raise PostGenerationFailureException("No Stop Sequence Found in Response")
        elif response.response_metadata["stop_sequence"] != "[GENERATION_SUCCESSFUL]":
            raise PostGenerationFailureException("Generation Failed: Invalid Prompt")
        
        post_title = ClaudeGenerationModel._extract_from_annotation(response.content, "title")

        post_text = ClaudeGenerationModel._extract_from_annotation(response.content, "content")

        return post_title, post_text

    @staticmethod
    def _extract_from_annotation(text: str, annotation: str=""):
        pattern = r"<" + re.escape(annotation) + r">(.*?)</" + re.escape(annotation) + r">"
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None