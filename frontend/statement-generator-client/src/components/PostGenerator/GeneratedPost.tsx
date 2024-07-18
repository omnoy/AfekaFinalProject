// GeneratedPost.tsx
import React, { useState } from 'react';
import { Box, Text, Textarea, Button, Group } from '@mantine/core';
import { IconCopy, IconCheck } from '@tabler/icons-react';
import { useTranslation } from 'react-i18next';

interface GeneratedPostProps {
  title: string | null;
  post: string | null;
}

export const GeneratedPost: React.FC<GeneratedPostProps> = ({ title, post }) => {
  const [copied, setCopied] = useState(false);
  const { t } = useTranslation('post_generator');

  const handleCopy = () => {
    if (post) {
      navigator.clipboard.writeText(post).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 5000);
      });
    }
  };

  return (
    <Box mt="xl">
      <Text fw={700} mah={600} mb="md">{title  || t('generated_post.post_title_placeholder')}</Text>
      <Textarea
        value={post || ''}
        placeholder={t('generated_post.post_text_placeholder')}
        minRows={6}
        readOnly
        autosize
        styles={(theme) => ({
          input: {
            backgroundColor: post ? theme.colors.gray[1] : theme.colors.dark[1],
            color: post ? theme.colors.gray[9] : theme.colors.dark[0]
          },
        })}
      />
      <Group mt="md">
        <Button 
          onClick={handleCopy}
          leftSection={copied ? <IconCheck size={16} /> : <IconCopy size={16} />}
          color={copied ? 'teal' : 'blue'}
          component="button"
        >
          {copied ? t('generated_post.copy_button_copied') : t('generated_post.copy_button')}
        </Button>
      </Group>
    </Box>
  );
};