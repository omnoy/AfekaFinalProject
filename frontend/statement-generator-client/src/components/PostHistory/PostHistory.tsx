import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, Anchor, NavLink, Loader, ScrollArea } from '@mantine/core';
import { IconCheck, IconCopy, IconArrowUp , IconArrowDown, IconStar  } from '@tabler/icons-react';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { getDateFromObjectId } from '@/services/getDateFromObjectId';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { IconStarFilled } from '@tabler/icons-react';

interface Post {
  id: string;
  title: string;
  text: string;
  publicOfficial: string;
  language: string;
  socialMedia: string;
  favorite: boolean;
  createdAt: Date;
}

export const PostHistory: React.FC = () => {
  const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({});
  const [posts, setPosts] = useState<Post[]>([]);
  const [postsDisplayedType, setPostsDisplayedType] = useState<'all' | 'favorites'>('all');
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken); 
  const {error, handleError, clearError, HTTPErrorComponent} = useHttpError();
  const { publicOfficials, loading, poError, refetch } = usePublicOfficials();
  const [poNames, setPONames] = useState<{id: string, name: string}[]>([]);
  const [isPONamesLoaded, setIsPONamesLoaded] = useState(false);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [loadingPosts, setLoadingPosts] = useState<boolean>(false);
  const [arePostsLoaded, setArePostsLoaded] = useState<boolean>(false);
  const [postsEmpty, setPostsEmpty] = useState<boolean>(false);
  const [favoritePostIDs, setFavoritePostIDs] = useState<string[]>([]);
  const { t } = useTranslation('post_generator');

  const getFavoritePostIDs = async () => {
    setLoadingPosts(true);
    try {
      const favorite_posts_response = await authApi.get('/user/favorites/generated_post');
      if (favorite_posts_response.status === 200) {
        console.log('Favorite posts:', favorite_posts_response);
        const favorite_posts = Array.from(favorite_posts_response.data.favorites);
         setFavoritePostIDs(favorite_posts.map((favorite_post: any) => favorite_post.id));
      } else {
        console.log('Error' + favorite_posts_response.data.error);
        handleError(new Error('Error: Unknown Error Loading Favorite Posts'));
      }
    } catch (error: any) {
      handleError(error);
    }
    finally {
      setLoadingPosts(false);
    }
  }

  const getPostHistoryByType = async (type : string) => {
    setLoadingPosts(true);
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
      const generated_posts_response = await authApi.get(url);

      if (generated_posts_response.status === 200) {
        console.log(type + 'Post History:', generated_posts_response.data);
        var generated_posts: any[] = [];
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
            publicOfficial: poNames.find((official) => official.id === generated_post.public_official_id)?.name,
            language: generated_post.language,
            socialMedia: generated_post.social_media,
            createdAt: getDateFromObjectId(generated_post.id)
          } as Post));
          return post_data;
      } else {
        console.log('Error' + generated_posts_response.data.error);
        handleError(new Error('Error: Unknown Error Loading Post History'));
      }
    } catch (error: any) {
      handleError(error);
    }
    finally {
      setLoadingPosts(false);
    }
    return [];
  }

  const handleAddFavorite = async (postId: string) => {
    console.log("Adding favorite post with id: " + postId);
    try {
      const response = await authApi.put('/user/favorites/generated_post/' + postId);
      if (response.status === 200) {
        console.log('Post favorited:', response.data);
        setFavoritePostIDs(prevIDs => [...prevIDs, postId]);
      } else {
        console.log('Error' + response.data.error);
        handleError(new Error('Error: Unknown Error Adding Favorite Post'));
      }
    } catch (error: any) {
      handleError(error);
    }
  }

  const handleRemoveFavorite = async (postId: string) => {
    console.log("Remove favorite post with id: " + postId);
    try {
      const response = await authApi.delete('/user/favorites/generated_post/' + postId);
      if (response.status === 200) {
        console.log('Post favorited:', response.data);
        setFavoritePostIDs(prevIDs => prevIDs.filter(id => id !== postId));
      } else {
        console.log('Error' + response.data.error);
        handleError(new Error('Error: Unknown Error Removing Favorite Post'));
      }
    } catch (error: any) {
      handleError(error);
    }
  }

  useEffect(() => {
    getFavoritePostIDs();
    getPostHistoryByType(postsDisplayedType);
  }, [postsDisplayedType]);

  useEffect(() => {
    if (publicOfficials.length > 0) {
      const names = publicOfficials.map((official: any) => ({id: official.id, name: official.name_eng}));
      setPONames(names);
      setIsPONamesLoaded(true);
    }
  }, [publicOfficials]);

  const fetchPostHistory = async () => {
    if (isPONamesLoaded) {
      const posts = await getPostHistoryByType(postsDisplayedType);
      if (sortDirection === 'desc'){
         posts.reverse(); //default sort by descending order
      }
      setPosts(posts);
      setArePostsLoaded(true);
    }
};

  useEffect(() => {
    fetchPostHistory();
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
    const postsEmpty = posts.length === 0;
    setPostsEmpty(postsEmpty);
  }
  checkPostsEmpty();
}, [posts]);


  const handleCopy = (postId: string, text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedStates(prev => ({ ...prev, [postId]: true }));
      setTimeout(() => {
        setCopiedStates(prev => ({ ...prev, [postId]: false }));
      }, 5000);
    });
  };
  
  return (
    <Box p="md">
      <Group justify="space-between" mb='md'>
        <Button onClick={() => {setPostsDisplayedType('all'); fetchPostHistory();}} variant='subtle'>
          <Title order={4} c={postsDisplayedType === 'all' ? 'blue' : 'dimmed'}>{t('post_history.all_history')}</Title>
        </Button>
        
        <Button onClick={() => {setPostsDisplayedType('favorites'); fetchPostHistory();}} variant='subtle'>
          <Title order={4} c={postsDisplayedType === 'favorites' ? 'blue' : 'dimmed'}>{t('post_history.favorite_history')}</Title>
        </Button>

        <Button onClick={() => setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')} variant='subtle'>
          {sortDirection === 'asc' ? 
            <IconArrowUp stroke={2}/>
            : 
            <IconArrowDown stroke={2}/>}
        </Button>
      </Group>
      <HTTPErrorComponent />
      <ScrollArea h={600} type='always'>
      {loadingPosts || loading || !arePostsLoaded ? 
      null
      :
      <Stack gap="lg">
        {postsEmpty && !loadingPosts && !loading && arePostsLoaded ? 
          postsDisplayedType === 'all' ?
          <Text>{t('post_history.no_posts_text')} <Link to='/generate'>{t('post_history.no_posts_link')}</Link> {t('post_history.no_posts_suffix')}</Text>
          :
          <Text>{t('post_history.no_favorites_text')}</Text>
        :
        posts.map((post) => (
          <Card key={post.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section withBorder inheritPadding py="xs">
              <Group justify="space-between">
                <Badge color="blue">{post.socialMedia}</Badge>
                <Text fw={500} dir={post.language === 'eng' ? 'ltr' : 'rtl'}>{post.title}</Text>
                { favoritePostIDs.includes(post.id) ? 
                <Button onClick={() => handleRemoveFavorite(post.id)}>
                  <IconStarFilled /> 
                </Button>
                : 
                <Button onClick={() => handleAddFavorite(post.id)}>
                  <IconStar />
                </Button>
                }
              </Group>
            </Card.Section>
            <Group justify="space-between">
              <Text mt="md" mb="xs" size="sm" c="dimmed">
                {t('generated_post.created_for')} {post.publicOfficial}
              </Text>
              <Text mt="md" mb="xs" size="sm" c="dimmed">
                {t('generated_post.language')}: {t('languages.' + post.language)}
              </Text>
            </Group>
            <Text size="sm" dir={post.language === 'eng' ? 'ltr' : 'rtl'} ta={post.language === 'eng' ? 'left' : 'right'}>
              {post.text}
            </Text>
            
            <Group mt="md" justify="space-between">
              <Text mt="md" size="xs" c="dimmed">
                {t('generated_post.created_on')} {post.createdAt.toLocaleString()}
              </Text>
              <Button
                onClick={() => handleCopy(post.id, post.text)}
                leftSection={copiedStates[post.id] ? <IconCheck size={16} /> : <IconCopy size={16} />}
                color={copiedStates[post.id] ? 'teal' : 'blue'}
              >
                {copiedStates[post.id] ? t('generated_post.copy_button_copied') : t('generated_post.copy_button')}
              </Button>
            </Group>
          </Card>
        ))
      }
      </Stack>
      }
    </ScrollArea>
    </Box>
  );
};