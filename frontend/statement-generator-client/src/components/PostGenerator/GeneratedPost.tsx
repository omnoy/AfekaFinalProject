// GeneratedPost.tsx
import React, { useState } from 'react';
import { Box, Text, Textarea, Button, Group } from '@mantine/core';
import { IconCopy, IconCheck } from '@tabler/icons-react';

interface GeneratedPostProps {
  post: string | null;
}

export const GeneratedPost: React.FC<GeneratedPostProps> = ({ post }) => {
  const [copied, setCopied] = useState(false);

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
      <Text fontWeight={700} mb="md">Your Generated Post:</Text>
      <Textarea
        value={post || ''}
        placeholder="Post output here"
        minRows={6}
        readOnly
        autosize
        styles={(theme) => ({
          input: {
            backgroundColor: post ? theme.colors.gray[1] : theme.colors.dark[1],
            color: post ? theme.colors.gray[9] : theme.colors.dark[0],
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
          {copied ? 'Copied!' : 'Copy to Clipboard'}
        </Button>
      </Group>
    </Box>
  );
};