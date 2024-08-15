from abc import ABC
import json
from os import getenv
from typing import List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

class BaseClaudeModel(ABC):
    # Base class for all Claude models, with methods to create a Claude Model instance and load a prompt template from file
    @staticmethod
    def get_claude_model(stop_sequences: List[str]):
        return ChatAnthropic(model=getenv("CLAUDE_MODEL_NAME"),
                            api_key=getenv("ANTHROPIC_API_KEY"),
                            max_tokens=4096, 
                            max_retries=3,
                            stop_sequences=stop_sequences)
        # Claude model instance is rebuilt each time the function is called so environment variables like the anthropics api key can be changed without restarting
    
    @staticmethod
    def _get_prompt_template(prompt_file_name: str) -> ChatPromptTemplate:
        prompt_template_dict = json.load(open(f"./app/prompts/{prompt_file_name}.json", "r"))
        
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