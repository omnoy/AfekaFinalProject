import json
from typing import Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import re
from os import getenv
from app.models.exceptions.post_generation_failure_exception import PostGenerationFailureException
import logging
from app.generation_model.base_claude_model import BaseClaudeModel

class ClaudeValidationModel(BaseClaudeModel):
    @staticmethod    
    def validate_post(generated_title: str, generated_text: str) -> str:
        
        prompt_template = ClaudeValidationModel._get_prompt_template("validation_prompt")
        # prompt template for the llm, where the variables will be inserted when invoked
        
        llm = ClaudeValidationModel.get_claude_model(stop_sequences=["[Y]", "[N]"])
        # claude llm model that generates the response  
        
        chain = (
            prompt_template # prompt template for llm
            | llm # llm model that generates a response
            | ClaudeValidationModel._validate_response #validates that response was successful
        )
        
        response_dict = chain.invoke({"title": generated_title, "content": generated_text})
        
        return response_dict
    
    @staticmethod
    def _validate_response(response) -> bool:
        
        logging.info(f"Validation Model Anthropic API response: {response}")
        
        response_dict = {"valid": "false", "reason": ""}
        
        if len(response.content) > 0:
            response_dict["reason"] = "Non-Empty Validation Response"
        elif response.response_metadata["stop_reason"] != "stop_sequence":
            response_dict["reason"] = "No Stop Sequence Found in Validation"
        elif response.response_metadata["stop_sequence"] != "[Y]":
            response_dict["reason"] = "Not A Valid Post"
        else:
            response_dict["valid"] = "true"
        
        return response_dict