from datetime import datetime

class PublicOfficial():
    def __init__(self,
                 _id: str,
                 personal_name: str,
                 position: str,
                 political_party: str,
                 trained_post_amount: int,
                 trained_post_start: datetime,
                 creation_date: datetime):
        self._id = _id
        self.personal_name = personal_name
        self.position = position
        self.political_party = political_party
        self.trained_post_amount = trained_post_amount
        self.trained_post_start = trained_post_start