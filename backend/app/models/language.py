from enum import StrEnum
import re
class Language(StrEnum):
    ENGLISH = "eng"
    HEBREW = "heb"    
    
    def get_full_name(self) -> str:
        full_names = {
            self.ENGLISH: "English",
            self.HEBREW: "Hebrew"
        }
        return full_names.get(self, "Unknown")
    
def string_language_validator(s: str, language: Language, allow_numbers: bool = False, allowed_symbols: str = "") -> bool: 
    pattern_string = ""
    
    if allow_numbers: 
        pattern_string += "0-9"
    if language == Language.ENGLISH:
        pattern_string += "a-zA-Z"
    elif language == Language.HEBREW:
        pattern_string += "\u0590-\u05fe"
    
    pattern_string += allowed_symbols
    
    pattern = re.compile(f"^({[pattern_string]}+)+$")
    return pattern.match(s)