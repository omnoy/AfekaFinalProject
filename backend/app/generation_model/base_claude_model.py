from abc import ABC
import json
from os import getenv
from typing import List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

class BaseClaudeModel(ABC):
    @staticmethod
    def get_claude_model(stop_sequences: List[str]):
        return ChatAnthropic(model=getenv("CLAUDE_MODEL_NAME"),
                            max_tokens=4096, 
                            max_retries=3,
                            stop_sequences=stop_sequences)
    
    @staticmethod
    def _get_prompt_template(prompt_file_name: str) -> ChatPromptTemplate:
        prompt_template_dict = json.load(open(f"./app/generation_model/prompts/{prompt_file_name}.json", "r"))
        
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