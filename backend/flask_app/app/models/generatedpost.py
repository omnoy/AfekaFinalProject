from datetime import datetime

class GeneratedPost():
    def __init__(self,
                 _id: str,
                 title: str,
                 user_id: str,
                 public_official_id: str,
                 prompt: str,
                 parameters: dict,
                 text: str,
                 social_media: str,
                 creation_date: datetime):
        self._id = _id
        self.title = title
        self.user_id = user_id
        self.public_official_id = public_official_id
        self.prompt = prompt
        self.parameters = parameters
        self.text = text
        self.social_media = social_media
        self.creation_date = creation_date