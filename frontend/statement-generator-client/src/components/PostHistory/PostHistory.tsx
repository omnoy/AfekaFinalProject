import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, Anchor, NavLink } from '@mantine/core';
import { IconCheck, IconCopy } from '@tabler/icons-react';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { getDateFromObjectId } from '@/services/getDateFromObjectId';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { Link } from 'react-router-dom';

interface Post {
  id: string;
  title: string;
  text: string;
  publicOfficial: string;
  socialMedia: string;
  createdAt: Date;
}

export const PostHistory: React.FC = () => {
  const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({});
  const [posts, setPosts] = useState<Post[]>([]);
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken); 
  const {error, handleError, clearError} = useHttpError();
  const { publicOfficials, loading, poError, refetch } = usePublicOfficials();
  const [poNames, setPONames] = useState<{id: string, name: string}[]>([]);
  const [isPONamesLoaded, setIsPONamesLoaded] = useState(false);

  const getPostHistory = async () => {
    // Fetch post history from the backend
    try {
      const response = await authApi.get('/post-generation/posts/user');
      if (response.status === 200) {
        console.log('Post History:', response.data);
        const generated_posts = Array.from(response.data.generated_posts);
        const post_data = generated_posts.map((generated_post: any) =>
          ({ 
            id: generated_post.id,
            title: generated_post.title,
            text: generated_post.text,
            publicOfficial: poNames.find((official) => official.id === generated_post.public_official_id)?.name,
            socialMedia: generated_post.social_media,
            createdAt: getDateFromObjectId(generated_post.id)
          } as Post));
          return post_data;
      } else {
        console.log('Error' + response.data.error);
        handleError(new Error('Error: Unknown Error loading Post History'));
      }
    } catch (error: any) {
      handleError(error);
    }
    return [];
  };

  useEffect(() => {
    if (publicOfficials.length > 0) {
      const names = publicOfficials.map((official: any) => ({id: official.id, name: official.name_eng}));
      setPONames(names);
      setIsPONamesLoaded(true);
    }
  }, [publicOfficials]);

  useEffect(() => {
    const fetchPostHistory = async () => {
        if (isPONamesLoaded) {
          const posts = await getPostHistory();

          setPosts(posts);
        }
    };

    fetchPostHistory();
}, [isPONamesLoaded]);

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
      <Title order={2} mb="xl">Your Generated Posts</Title>
      <Stack gap="lg">
        {posts.length ? 
        posts.map((post) => (
          <Card key={post.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section withBorder inheritPadding py="xs">
              <Group justify="center">
                <Text fw={500} dir='rtl'>{post.title}</Text>
                <Badge color="blue">{post.socialMedia}</Badge>
              </Group>
            </Card.Section>

            <Text mt="md" mb="xs" size="sm" color="dimmed">
              Created for: {post.publicOfficial}
            </Text>
            
            <Text size="sm" dir='rtl' ta='right'>{post.text}</Text>
            <Group mt="md" justify="space-between">
              <Text mt="md" size="xs" color="dimmed">
                Created on: {post.createdAt.toLocaleString()}
              </Text>
              <Button
                onClick={() => handleCopy(post.id, post.text)}
                leftSection={copiedStates[post.id] ? <IconCheck size={16} /> : <IconCopy size={16} />}
                color={copiedStates[post.id] ? 'teal' : 'blue'}
              >
                {copiedStates[post.id] ? 'Copied!' : 'Copy to Clipboard'}
              </Button>
            </Group>
          </Card>
        ))
      :
        <Text>No posts found! Go to <Link to='/generate'>the post generator</Link> to get started!</Text>}
      </Stack>
    </Box>
  );
};