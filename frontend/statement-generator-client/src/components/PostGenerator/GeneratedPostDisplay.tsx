// GeneratedPost.tsx
import React, { useState } from 'react';
import { Box, Text, Textarea, Button, Group } from '@mantine/core';
import { IconCopy, IconCheck, IconStarFilled, IconStar } from '@tabler/icons-react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { useHttpError } from '@/hooks/useHttpError';
import { GeneratedPost } from '@/types/GeneratedPost';

interface GeneratedPostDisplayProps {
  post: GeneratedPost | undefined;
}

export const GeneratedPostDisplay: React.FC<GeneratedPostDisplayProps> = ({ post }) => {
  const [copied, setCopied] = useState(false);
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken);
  const { t, i18n } = useTranslation('post_generator');
  const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
  const [ isFavorite, setIsFavorite ] = useState(false);

  const handleCopy = () => {
    if (post) {
      navigator.clipboard.writeText(post.text).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 5000);
      });
    }
  };

  const handleAddFavorite = async (postId: string) => {
    console.log("Adding favorite post with id: " + postId);
    try {
      const response = await authApi.put('/user/favorites/generated_post/' + postId);
      if (response.status === 200) {
        console.log('Post favorited:', response.data);
        setIsFavorite(true);
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
        setIsFavorite(false);
      } else {
        console.log('Error' + response.data.error);
        handleError(new Error('Error: Unknown Error Removing Favorite Post'));
      }
    } catch (error: any) {
      handleError(error);
    }
  }


  return (
    <Box mt="xl">
      <Text fw={700} mah={600} mb="md" dir={post?.language ? 
                                            post.language === 'eng' ? 'ltr' : 'rtl'
                                            : i18n.language === 'eng' ? 'ltr' : 'rtl' 
                                            }>
        {post?.title  || t('generated_post.post_title_placeholder')}
      </Text>
      <Textarea
        value={post?.text || ''}
        placeholder={t('generated_post.post_text_placeholder')}
        minRows={6}
        readOnly
        autosize
        dir={ post === undefined ?
          i18n.language === 'eng' ? 'ltr' : 'rtl' 
          : post?.language === 'eng' ? 'ltr' : 'rtl'
        }
        styles={(theme) => ({
          input: {
            backgroundColor: post ? theme.colors.gray[1] : theme.colors.dark[1],
            color: post ? theme.colors.gray[9] : theme.colors.dark[0],
            textAlign: post === undefined ? i18n.language === 'eng' ? 'left' : 'right' : post?.language === 'eng' ? 'left' : 'right'
          },
        })}
      />
      { post &&
        <Group mt="md" justify='space-between'>
          <Button 
            onClick={handleCopy}
            leftSection={copied ? <IconCheck size={16} /> : <IconCopy size={16} />}
            color={copied ? 'teal' : 'blue'}
            component="button"
          >
            {copied ? t('generated_post.copy_button_copied') : t('generated_post.copy_button')}
          </Button>
          { isFavorite ?
            <Button onClick={() => handleRemoveFavorite(post.id)}>
              <IconStarFilled /> 
            </Button>
            : 
            <Button onClick={() => handleAddFavorite(post.id)}>
              <IconStar />
            </Button>
          }
        </Group>
      }
      <HTTPErrorComponent />
    </Box>
  );
};