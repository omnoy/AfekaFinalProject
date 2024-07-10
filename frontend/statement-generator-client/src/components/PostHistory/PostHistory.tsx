import React, { useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button } from '@mantine/core';
import { IconCheck, IconCopy } from '@tabler/icons-react';

interface Post {
  id: string;
  title: string;
  text: string;
  publicOfficial: string;
  socialMedia: string;
  createdAt: Date;
}

const mockPosts: Post[] = [
  {
    id: '1',
    title: 'Climate Change Initiative',
    text: "We're taking bold steps to address climate change. Our new initiative aims to reduce carbon emissions by 30% over the next five years.",
    publicOfficial: 'Benyamin Netanyahu',
    socialMedia: 'Twitter',
    createdAt: new Date('2024-07-08T10:30:00'),
  },
  {
    id: '2',
    title: 'Education Budget Increase',
    text: "I'm proud to announce a significant increase in our education budget. This will support our teachers and provide better resources for our students.",
    publicOfficial: 'Mr. Frog',
    socialMedia: 'Facebook',
    createdAt: new Date('2024-07-07T14:45:00'),
  },
  {
    id: '3',
    title: 'New Job Creation Program',
    text: "Our administration is launching a new job creation program aimed at boosting employment in key sectors. Let's build a stronger economy together!",
    publicOfficial: 'President Jimble',
    socialMedia: 'LinkedIn',
    createdAt: new Date('2024-07-06T09:15:00'),
  },
];

export const PostHistory: React.FC = () => {
  const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({});

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
        {mockPosts.map((post) => (
          <Card key={post.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section withBorder inheritPadding py="xs">
              <Group justify="center">
                <Text fontWeight={500}>{post.title}</Text>
                <Badge color="blue">{post.socialMedia}</Badge>
              </Group>
            </Card.Section>

            <Text mt="md" mb="xs" size="sm" color="dimmed">
              Created for: {post.publicOfficial}
            </Text>
            
            <Text size="sm">{post.text}</Text>
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
        ))}
      </Stack>
    </Box>
  );
};