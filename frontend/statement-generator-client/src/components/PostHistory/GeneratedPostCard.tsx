import { favoriteObjectType } from "@/hooks/useFavorites";
import { GeneratedPost } from "@/types/GeneratedPost";
import { Box, Text, Card, Stack, Group, Badge, Title, Button, Anchor, NavLink, Loader, ScrollArea, Spoiler, Blockquote } from '@mantine/core';
import { IconCheck, IconCopy, IconArrowUp , IconArrowDown, IconStar, IconStarFilled  } from '@tabler/icons-react';
import { useState } from "react";
import { useTranslation } from "react-i18next";

interface GeneratedPostCardProps {
    post: GeneratedPost;
    favoriteObjectIDs: string[];
    handleAddFavorite: (type: favoriteObjectType, postId: string) => Promise<void>;
    handleRemoveFavorite: (type: favoriteObjectType, postId: string) => Promise<void>;
}

export const GeneratedPostCard: React.FC<GeneratedPostCardProps> = ({post, favoriteObjectIDs, handleAddFavorite, handleRemoveFavorite}) => {
    const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({});
    const { t, i18n } = useTranslation('post_generator');

    const handleCopy = (postId: string, text: string) => {
        navigator.clipboard.writeText(text).then(() => {
          setCopiedStates(prev => ({ ...prev, [postId]: true }));
          setTimeout(() => {
            setCopiedStates(prev => ({ ...prev, [postId]: false }));
          }, 5000);
        });
      };

    return (
        <Card key={post.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section withBorder inheritPadding py="xs">
              <Group justify="space-between">
                <Badge color="blue">{post.socialMedia}</Badge>
                <Text fw={500} dir={post.language === 'eng' ? 'ltr' : 'rtl'}>{post.title}</Text>
                { favoriteObjectIDs.includes(post.id) ? 
                <Button onClick={() => handleRemoveFavorite({type: "generated_post"}, post.id)}>
                  <IconStarFilled /> 
                </Button>
                : 
                <Button onClick={() => handleAddFavorite({type: "generated_post"}, post.id)}>
                  <IconStar />
                </Button>
                }
              </Group>
            </Card.Section>
            <Group justify="space-between">
              <Text mt="md" mb="xs" size="sm" c="dimmed">
                {t('generated_post.created_for')} {i18n.language === 'eng' ? post.publicOfficialName?.eng : post.publicOfficialName?.heb}
              </Text>
              <Text mt="md" mb="xs" size="sm" c="dimmed">
                {t('generated_post.language')}: {t(`languages.${post.language}`)}
              </Text>
            </Group>
            
            <Text size="sm" dir={post.language === 'eng' ? 'ltr' : 'rtl'} ta={post.language === 'eng' ? 'left' : 'right'}>
              {post.text}
            </Text>

            <Spoiler maxHeight={0} showLabel={t('generated_post.show_prompt')} hideLabel={t('generated_post.hide_prompt')} mt="md">
              <Blockquote color="blue" radius="xl" dir={post.language === 'eng' ? 'ltr' : 'rtl'} ta={post.language === 'eng' ? 'left' : 'right'}>
                {post.prompt}
              </Blockquote>
            </Spoiler>

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
    )
}
