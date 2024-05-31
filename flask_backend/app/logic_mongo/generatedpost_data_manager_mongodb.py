from bson import ObjectId
from typing import Optional
from app.extensions import mongo, generation_model
from app.generation_model.generation_model import GenerationModel
from app.models.generatedpost import GeneratedPost
from app.models.social_media import SocialMedia
from app.logic.generatedpost_service import GeneratedPostService

class GeneratedPostDataManagerMongoDB(GeneratedPostService):
    def __init__(self) -> None:
        self.generated_post_collection = mongo.db["generatedposts"] 
        self.user_collection = mongo.db["users"]
        self.po_collection = mongo.db["public_officials"]
        self.generation_model = generation_model

    def generate_post(self, generation_prompt: str, po_id: str, 
                      user_id: Optional[str] = None, social_media: Optional[SocialMedia] = None) -> GeneratedPost:
        
        public_official = self.po_collection.find_one({"_id": ObjectId(po_id)})
        generated_text = self.generation_model.generate_post(generation_prompt=generation_prompt,
                                                             public_official=public_official,
                                                             social_media=social_media)

        generated_post = GeneratedPost(user_id=user_id, 
                                       public_official_id=po_id,
                                       title="jeffpost", #TODO fix 
                                       text=generated_text,
                                       prompt=generation_prompt,
                                       social_media=SocialMedia.FACEBOOK)

        inserted_obj = self.generated_post_collection.insert_one(generated_post.model_dump(exclude='id'))
        generated_post.id = inserted_obj.inserted_id

        return generated_post

    def get_generated_post_by_id(self, post_id: str) -> GeneratedPost:
        post_dict = self.generated_post_collection.find_one({"_id":ObjectId(post_id)})
        generated_post = GeneratedPost(**post_dict)

        return generated_post

    def get_generated_posts_by_user_id(self, user_id: str) -> list[GeneratedPost]:
        post_dicts = self.generated_post_collection.find({"user_id":ObjectId(user_id)})
        post_list = list()
        
        for post_dict in post_dicts:
            post_list.append(GeneratedPost(**post_dict))
        
        return post_list

    def get_generated_posts_by_public_official_id(self, po_id: str) -> list[GeneratedPost]:
        post_dicts = self.generated_post_collection.find({"public_official_id":ObjectId(po_id)})
        post_list = list()
        
        for post_dict in post_dicts:
            post_list.append(GeneratedPost(**post_dict))
        
        return post_list

    def get_all_generated_posts(self) -> list[GeneratedPost]:
        post_dicts = self.generated_post_collection.find()
        post_list = list()
        
        for post_dict in post_dicts:
            post_list.append(GeneratedPost(**post_dict))
        
        return post_list

    def delete_all_generated_posts(self) -> None:
        self.generated_post_collection.delete_many({})