from typing import Optional, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import re
from os import getenv
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.generation_model.generation_model import GenerationModel
from app.models.language import Language
import logging

class ClaudeModel(GenerationModel):
    @staticmethod    
    def generate_post(generation_prompt: str, public_official: PublicOfficial, language: Language,
                        social_media: Optional[SocialMedia]) -> str:
        llm = ChatAnthropic(model=getenv("CLAUDE_MODEL_NAME"),
                            max_tokens=4096, 
                            max_retries=3,
                            stop_sequences=["[GENERATION_SUCCESSFUL]", "[GENERATION_FAILED]"])
        
        prompt = ClaudeModel._get_prompt()

        chain = prompt | llm

        if social_media is None:
            social_media = "social media"

        response = ClaudeModel._get_api_response(chain, generation_prompt, public_official, language, social_media)
        
        logging.info(f"Anthropic API response: {response}")
        
        if response.response_metadata["stop_reason"] != "stop_sequence":
            raise PostGenerationFailureException("No Stop Sequence Found in Response")
        elif response.response_metadata["stop_sequence"] != "[GENERATION_SUCCESSFUL]":
            raise PostGenerationFailureException("Generation Failed: Invalid Prompt")
            

        post_title, post_text = ClaudeModel._process_response(response.content)

        return post_title, post_text

    @staticmethod
    def get_model_type() -> str:
        return "Claude"
    
    @staticmethod
    def _get_prompt() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    '''
                    As a {SOCIAL_MEDIA} post generator for posts in the {LANGUAGE} language, your task is to write a {SOCIAL_MEDIA} post in {LANGUAGE} for {PUBLIC_OFFICIAL_ROLE} {PUBLIC_OFFICIAL}’s {SOCIAL_MEDIA}, according to the prompt passed to you, contained within the following tags: <prompt> </prompt>.

                    {PUBLIC_OFFICIAL} is a/the {PUBLIC_OFFICIAL_ROLE}.
                    {PUBLIC_OFFICIAL_INFORMATION} 

                    Generate the {SOCIAL_MEDIA} post according to {PUBLIC_OFFICIAL}’s opinions and role. The social media post should feel natural and fluent according to the information. 
                    
                    Contain the content of the post between the following tags: <content> </content>. 

                    Give the post a title that is relevant to the content of the post. Contain the title between the following tags: <title> </title>.

                    Upon successful generation, please include the phrase [GENERATION_SUCCESSFUL] at the end and only at the end of your response to indicate a successful post generation. If the post generation fails for whatever reason, only include the phrase [GENERATION_FAILED].

                    Provide a response without any additional information or comments besides the previously stated phrase.
                    '''
                ),
                ("human", "<prompt> {input} </prompt>")
            ]
        )
    
    @staticmethod
    def _get_api_response(chain, generation_prompt: str, public_official: PublicOfficial, language: Language, social_media: Optional[SocialMedia]) -> str:
        response = chain.invoke(
            {
                "SOCIAL_MEDIA": str(social_media),
                "PUBLIC_OFFICIAL_ROLE": public_official.position,
                "PUBLIC_OFFICIAL": public_official.name_eng,
                "PUBLIC_OFFICIAL_INFORMATION": f"{public_official.name_eng} is a member of the {public_official.political_party}.",
                "LANGUAGE": language.get_full_name(),
                "input": generation_prompt
            }
        )

        return response
    
    @staticmethod
    def _process_response(response_content: str) -> Tuple[str]:
        post_title = ClaudeModel._extract_from_annotation(response_content, "title")

        post_text = ClaudeModel._extract_from_annotation(response_content, "content")

        return post_title, post_text

    @staticmethod
    def _extract_from_annotation(text: str, annotation: str=""):
        pattern = r"<" + re.escape(annotation) + r">(.*?)</" + re.escape(annotation) + r">"
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None