import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, ScrollArea } from '@mantine/core';
import { IconStar, IconStarFilled, IconBrandFacebook, IconBrandTwitter, IconBrandInstagram, IconBrandLinkedin } from '@tabler/icons-react';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { useTranslation } from 'react-i18next';
import { SocialMediaHandle } from '@/types/SocialMediaHandle';
import { PublicOfficial } from '@/types/PublicOfficial';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';

const SocialMediaIcon: React.FC<{ platform: string }> = ({ platform }) => {
  switch (platform.toLowerCase()) {
    case 'facebook': return <IconBrandFacebook size={16} />;
    case 'twitter': return <IconBrandTwitter size={16} />;
    case 'instagram': return <IconBrandInstagram size={16} />;
    case 'linkedin': return <IconBrandLinkedin size={16} />;
    default: return null;
  }
};

export const PublicOfficialsDisplay: React.FC = () => {
  const { publicOfficials, loading, refetch } = usePublicOfficials();
  const [favoriteOfficialIDs, setFavoriteOfficialIDs] = useState<string[]>([]);
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken);
  const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
  const { t, i18n } = useTranslation('public_officials');

  const getFavoriteOfficials = async () => {
    try {
      const response = await authApi.get('/user/favorites/public_official');
      if (response.status === 200) {
        const favoriteOfficials = Array.from(response.data.favorites);
        setFavoriteOfficialIDs(favoriteOfficials.map((official: any) => official.id));
      } else {
        handleError(new Error('Error: Unknown Error Loading Favorite Officials'));
      }
    } catch (error: any) {
      handleError(error);
    }
  };

  const handleAddFavorite = async (officialId: string) => {
    try {
      const response = await authApi.put(`/user/favorites/public_official/${officialId}`);
      if (response.status === 200) {
        setFavoriteOfficialIDs(prevIDs => [...prevIDs, officialId]);
      } else {
        handleError(new Error('Error: Unknown Error Adding Favorite Official'));
      }
    } catch (error: any) {
      handleError(error);
    }
  };

  const handleRemoveFavorite = async (officialId: string) => {
    try {
      const response = await authApi.delete(`/user/favorites/public_official/${officialId}`);
      if (response.status === 200) {
        setFavoriteOfficialIDs(prevIDs => prevIDs.filter(id => id !== officialId));
      } else {
        handleError(new Error('Error: Unknown Error Removing Favorite Official'));
      }
    } catch (error: any) {
      handleError(error);
    }
  };

  useEffect(() => {
    getFavoriteOfficials();
    refetch();
  }, []);

  return (
    <Box p="md">
      <Title order={2} mb="xl">{t('all_officials_title')}</Title>
      <HTTPErrorComponent />
      <ScrollArea h={600} type='always'>
        {loading ? (
          <Text>{t('loading')}</Text>
        ) : (
          <Stack gap="lg">
            {publicOfficials.map((official) => (
              <Card key={official.id} shadow="sm" padding="lg" radius="md" withBorder>
                <Card.Section withBorder inheritPadding py="xs">
                  <Group justify="space-between">
                    <Text fw={500}>
                      {i18n.language === 'eng' ? official.full_name.eng : official.full_name.heb} ({i18n.language === 'eng' ? official.full_name.heb : official.full_name.eng})
                    </Text>
                    <Button
                      onClick={() => favoriteOfficialIDs.includes(official.id) 
                        ? handleRemoveFavorite(official.id) 
                        : handleAddFavorite(official.id)
                      }
                    >
                      {favoriteOfficialIDs.includes(official.id) ? <IconStarFilled /> : <IconStar />}
                    </Button>
                  </Group>
                </Card.Section>

                <Text mt="md" mb="xs">
                  <Text span fw={700}>{t('position')}: </Text>
                  {i18n.language === 'eng' ? official.position.eng : official.position.heb}
                </Text>

                {official.age !== null && (
                  <Text mb="xs">
                    <Text span fw={700}>{t('age')}: </Text>
                    {official.age}
                  </Text>
                )}

                {official.political_party !== null && (
                <Text mb="xs">
                  <Text span fw={700}>{t('political_party')}: </Text>
                  {i18n.language === 'eng' ? official.political_party?.eng : official.political_party?.heb}
                </Text>
                )}
                {/* <Group gap="xs" mb="xs">
                  <Text fw={700}>{t('social_media')}:</Text>
                  {official.social_media_handles.map((handle, index) => (
                    <Badge
                      key={index}
                      leftSection={<SocialMediaIcon platform={handle.social_media} />}
                      variant="outline"
                    >
                      {handle.handle}
                    </Badge>
                  ))}
                </Group> */}
              </Card>
            ))}
          </Stack>
        )}
      </ScrollArea>
    </Box>
  );
};