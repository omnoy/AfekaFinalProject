from app.models.publicofficial import PublicOfficial

class PublicOfficialService:
    
    def __init__(self) -> None:
        "Initialize Public Official Database"
        pass   

    def create_public_official(self, public_official: PublicOfficial) -> PublicOfficial:
        "Create a Public Official for the Database using a PublicOfficial class"
        pass

    def get_public_official_by_id(self, public_official_id: str) -> PublicOfficial:
        "Get a PO by their ID"
        pass

    def update_public_official(self, public_official_id: str, public_official: PublicOfficial) -> PublicOfficial:
        "Update a PublicOfficial according to the parameters"
        pass

    def get_all_public_officials(self) -> list[PublicOfficial]:
        "Get all PublicOfficials from the database"
        pass

    def delete_all_public_officials(self) -> None:
        "Delete all public_officials from the database"
        pass