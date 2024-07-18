from bson import ObjectId
from typing import Optional
from app.extensions import generation_model
from app.generation_model.generation_model import GenerationModel
from app.models.generatedpost import GeneratedPost
from app.models.publicofficial import PublicOfficial
from app.models.social_media import SocialMedia
from app.logic.generatedpost_service import GeneratedPostService
from app.logic.mongo.database import get_public_official_collection, get_generated_post_collection
from app.extensions import logger
from app.models.language import Language

class GeneratedPostDataManagerMongoDB(GeneratedPostService):
    def __init__(self) -> None:
        pass

    def generate_post(self, generation_prompt: str, public_official_id: str, 
                      user_id: str, language: Language, social_media: SocialMedia) -> GeneratedPost:
        if len(generation_prompt) == 0 or generation_prompt.isspace():
            raise ValueError("Generation prompt cannot be empty")
        if language is not None and language not in Language:
            raise ValueError("Invalid post language")
        
        if social_media is not None and social_media not in SocialMedia:
            raise ValueError("Invalid social media type")

        public_official = get_public_official_collection().find_one({"_id": ObjectId(public_official_id)})
        if public_official is None:
            raise KeyError(f"Public Official with ID {public_official_id} not found")
        
        generated_title, generated_text = generation_model.generate_post(generation_prompt=generation_prompt,
                                                                            public_official=PublicOfficial(**public_official),
                                                                            language=Language(language),
                                                                            social_media=SocialMedia(social_media))
        
        if not generated_title:
            generated_title = "Untitled"

        logger.info(f"Generated Post Title: {generated_title}, Text: {generated_text}")
        generated_post = GeneratedPost(user_id=ObjectId(user_id), 
                                       public_official_id=ObjectId(public_official_id),
                                       title=generated_title,
                                       text=generated_text,
                                       prompt=generation_prompt,
                                       language=language,
                                       social_media=social_media)

        inserted_obj = get_generated_post_collection().insert_one(generated_post.model_dump(exclude='id'))
        generated_post.id = inserted_obj.inserted_id

        return generated_post

    def get_generated_post_by_id(self, post_id: str) -> GeneratedPost:
        post_dict = get_generated_post_collection().find_one({"_id":ObjectId(post_id)})
        if post_dict is None:
            return None
        
        generated_post = GeneratedPost(**post_dict)

        return generated_post

    def get_generated_posts_by_user_id(self, user_id: str) -> list[GeneratedPost]:
        post_dicts = get_generated_post_collection().find({"user_id":user_id})
        post_list = list()
        
        if post_dicts is None:
            return post_list #return empty list if no posts found
        
        for post_dict in post_dicts:
            post_list.append(GeneratedPost(**post_dict))
        
        return post_list

    def get_all_generated_posts(self) -> list[GeneratedPost]:
        post_dicts = get_generated_post_collection().find()
        post_list = list()
        if post_dicts is None:
            return post_list
        
        for post_dict in post_dicts:
            post_list.append(GeneratedPost(**post_dict))
        
        return post_list

    def delete_all_generated_posts(self) -> None:
        get_generated_post_collection().delete_many({})