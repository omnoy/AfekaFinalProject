import { useAuth } from "@/context/AuthProvider";
import { createAuthApi } from "@/services/api";
import { useHttpError } from "./useHttpError";
import { useState } from "react";

interface favoriteObjectType {
    type: 'generated_post' | 'public_official';
}

export const useFavoriteObjects = () => {
    const { accessToken } = useAuth();
    const authApi = createAuthApi(accessToken);
    const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
    const [favoriteObjectIDs, setFavoriteObjectIDs] = useState<string[]>([]);[]
    
    const getFavoriteObjectIDs = async (type: favoriteObjectType) => {
        try {
          const favorite_objects_response = await authApi.get(`user/favorites/${type.type}`);
          if (favorite_objects_response.status === 200) {
            console.log(`Favorite object of type ${type}:`, favorite_objects_response);
            const favorite_objects = Array.from(favorite_objects_response.data.favorites);
            setFavoriteObjectIDs(favorite_objects.map((favorite_object: any) => favorite_object.id));

          } else {
            console.log('Error' + favorite_objects_response.data.error);
            handleError(new Error('Error: Unknown Error Loading Favorite Objects'));
          }
        } catch (error: any) {
          handleError(error);
        }
    }

    const handleAddFavorite = async (type: favoriteObjectType, object_id: string) => {
        console.log(`Adding favorite ${type} with id: ${object_id}`);
        try {
          const response = await authApi.put(`/user/favorites/${type.type}/${object_id}`);
          if (response.status === 200) {
            console.log('Object favorited:', response.data);
            setFavoriteObjectIDs(prevIDs => [...prevIDs, object_id]);
          } else {
            console.log('Error' + response.data.error);
            handleError(new Error('Error: Unknown Error Adding Favorite Object'));
          }
        } catch (error: any) {
          handleError(error);
        }
      }
    
      const handleRemoveFavorite = async (type: favoriteObjectType, object_id: string) => {
        console.log(`Removing favorite ${type} with id: ${object_id}`);
        try {
          const response = await authApi.delete(`/user/favorites/${type.type}/${object_id}`);
          if (response.status === 200) {
            console.log('Object removed from favorites:', response.data);
            setFavoriteObjectIDs(prevIDs => prevIDs.filter(id => id !== object_id));
          } else {
            console.log('Error' + response.data.error);
            handleError(new Error('Error: Unknown Error Removing Favorite Object'));
          }
        } catch (error: any) {
          handleError(error);
        }
      }
      return { favoriteObjectIDs, getFavoriteObjectIDs, handleAddFavorite, handleRemoveFavorite };
};