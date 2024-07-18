from enum import StrEnum

class Language(StrEnum):
    ENGLISH = "eng"
    HEBREW = "heb"    
    
    def get_full_name(self) -> str:
        full_names = {
            self.ENGLISH: "English",
            self.HEBREW: "Hebrew"
        }
        return full_names.get(self, "Unknown")