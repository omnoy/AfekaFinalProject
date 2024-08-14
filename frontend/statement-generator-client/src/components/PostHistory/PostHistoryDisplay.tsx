import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, Anchor, NavLink, Loader, ScrollArea, Center } from '@mantine/core';
import { IconArrowUp , IconArrowDown  } from '@tabler/icons-react';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { getDateFromObjectId } from '@/services/getDateFromObjectId';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { GeneratedPost } from '@/types/GeneratedPost';
import { useFavoriteObjects } from '@/hooks/useFavorites';
import { GeneratedPostCard } from './GeneratedPostCard';
import { ObjectDisplayContainer } from '../ObjectDisplayContainer/ObjectDisplayContainer';

export const PostHistory: React.FC = () => {
  const [posts, setPosts] = useState<GeneratedPost[]>([]);
  const [postsDisplayedType, setPostsDisplayedType] = useState<'all' | 'favorites'>('all');
  const { getAccessToken  } = useAuth();
  const authApi = createAuthApi(getAccessToken()); 
  const {error, handleError, clearError, HTTPErrorComponent} = useHttpError();
  const { publicOfficials, loadingPublicOfficials, poError, fetchPublicOfficials } = usePublicOfficials();
  const { getFavoriteObjectIDs, favoriteObjectIDs, handleAddFavorite, handleRemoveFavorite } = useFavoriteObjects();
  const [poNames, setPONames] = useState<{id: string, name: {eng: string, heb: string}}[]>([]);
  const [isPONamesLoaded, setIsPONamesLoaded] = useState(false);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [arePostsLoaded, setArePostsLoaded] = useState<boolean>(false);
  const [postsEmpty, setPostsEmpty] = useState<boolean>(false);

  const { t } = useTranslation('post_generator');

  const getPostHistoryByType = async (type : 'all' | 'favorites') => {
    try {
      var url = '';
      if (type === 'all') {
        url = '/post-generation/posts/user';
      }
      else if(type === 'favorites') {
        url = '/user/favorites/generated_post';
      }
      else {
        handleError(new Error('Error: Unknown Post Type'));
      }
      const generated_posts_response = await authApi?.get(url);

      if (generated_posts_response.status === 200) {
        console.log(type + 'Post History:', generated_posts_response.data);
        var generated_posts: GeneratedPost[] = [];
        if (type === 'all') {
          generated_posts = Array.from(generated_posts_response.data.generated_posts);
        }
        else if(type === 'favorites') {
          generated_posts = Array.from(generated_posts_response.data.favorites);
        }
        else {
          handleError(new Error('Error: Unknown Post Type'));
        }
        const post_data = generated_posts.map((generated_post: any) =>
          ({ 
            id: generated_post.id,
            title: generated_post.title,
            text: generated_post.text,
            prompt: generated_post.prompt,
            publicOfficialName: poNames.find((official) => official.id === generated_post.public_official_id)?.name,
            language: generated_post.language,
            socialMedia:t('social_media.' + generated_post.social_media),
            createdAt: getDateFromObjectId(generated_post.id)
          } as GeneratedPost));
          return post_data;
      } else {
        console.log('Error' + generated_posts_response.data.error);
        handleError(new Error('Error: Unknown Error Loading Post History'));
      }
    } catch (error: any) {
      handleError(error);
    }
    return [];
  }

  useEffect(() => {
    fetchPublicOfficials('all');
  }, []);

  useEffect(() => {
    if (publicOfficials.length > 0) {
      const names = publicOfficials.map((official: any) => ({
        id: official.id, 
        name: {
          eng: official.full_name.eng, 
          heb: official.full_name.heb 
        }
      }));  
      setPONames(names);
      setIsPONamesLoaded(true);
    }
  }, [publicOfficials]);

  const fetchPostHistory = async () => {
    if (isPONamesLoaded) {
      getFavoriteObjectIDs({type: 'generated_post'});
      const posts = await getPostHistoryByType(postsDisplayedType);
      if (sortDirection === 'asc'){
         posts.reverse(); //default sort by asc order
      }
      setPosts(posts);
    }
  };

  useEffect(() => {
    const loadPosts = async () => {
      try {
        if (isPONamesLoaded) {
          setArePostsLoaded(false);
          await fetchPostHistory();
          setArePostsLoaded(true);
        }
      } catch (error: any) {
        setArePostsLoaded(false);
      }
    }
  
    loadPosts();
  }, [isPONamesLoaded, postsDisplayedType]);

useEffect(()=> {
  const sortPosts = () => {
    const sortedPosts = posts.reverse();
    setPosts([...sortedPosts]);
  }
  sortPosts();
}, [sortDirection]);

useEffect(() => {
  const checkPostsEmpty = () => {
    if (arePostsLoaded) {
      setPostsEmpty(posts.length === 0);
    }
  }
  checkPostsEmpty();
}, [posts]);
  
  return (
    <Box p="md">
      <ObjectDisplayContainer objectsDisplayedType={postsDisplayedType} setObjectsDisplayedType={setPostsDisplayedType} sortDirection={sortDirection} setSortDirection={setSortDirection} />
      <HTTPErrorComponent />
      <ScrollArea h={600} type='always'>
      {!arePostsLoaded || loadingPublicOfficials ?
      <Center>
        <Loader />
      </Center>
      :
      <Stack gap="lg">
        {arePostsLoaded && postsEmpty ? 
          postsDisplayedType === 'all' ?
          <Text>{t('post_history.no_posts_text')} <Link to='/generate'>{t('post_history.no_posts_link')}</Link> {t('post_history.no_posts_suffix')}</Text>
          :
          <Text>{t('post_history.no_favorites_text')}</Text>
        :
        posts.map((post) => (
          <GeneratedPostCard key={post.id} post={post} favoriteObjectIDs={favoriteObjectIDs} handleAddFavorite={handleAddFavorite} handleRemoveFavorite={handleRemoveFavorite} />
        ))
      }
      </Stack>
      }
    </ScrollArea>
    </Box>
  );
};