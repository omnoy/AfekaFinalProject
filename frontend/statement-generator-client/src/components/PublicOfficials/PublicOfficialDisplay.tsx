import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, ScrollArea } from '@mantine/core';
import { IconStar, IconStarFilled, IconBrandFacebook, IconBrandTwitter, IconBrandInstagram, IconBrandLinkedin } from '@tabler/icons-react';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { useTranslation } from 'react-i18next';
import { PublicOfficial } from '@/types/PublicOfficial';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { getDateFromObjectId } from '@/services/getDateFromObjectId';
import { useFavoriteObjects } from '@/hooks/useFavorites';

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
  const { publicOfficials, loadingPublicOfficials, fetchPublicOfficials } = usePublicOfficials();
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken);
  const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
  const { t, i18n } = useTranslation('public_officials');
  const [publicOfficialsDisplayedType, setPublicOfficialsDisplayedType] = useState<'all' | 'favorites'>('all');
  const { getFavoriteObjectIDs, favoriteObjectIDs, handleAddFavorite, handleRemoveFavorite } = useFavoriteObjects();

  useEffect(() => {
    getFavoriteObjectIDs({type: 'public_official'});
    console.log(publicOfficials)
    fetchPublicOfficials();
  }, []);

  return (
    <Box p="md">
      <Group justify="space-between" mb='md'>
      <Button onClick={() => {setPublicOfficialsDisplayedType('all');}} variant='subtle'>
          <Title order={4} c={publicOfficialsDisplayedType === 'all' ? 'blue' : 'dimmed'}>{t('all_officials_title')}</Title>
        </Button>
        
        <Button onClick={() => {setPublicOfficialsDisplayedType('favorites');}} variant='subtle'>
          <Title order={4} c={publicOfficialsDisplayedType === 'favorites' ? 'blue' : 'dimmed'}>{t('favorite_officials_title')}</Title>
        </Button>
      </Group>
      <HTTPErrorComponent />
      <ScrollArea h={600} type='always'>
        {loadingPublicOfficials ? (
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
                      onClick={() => favoriteObjectIDs.includes(official.id) 
                        ? handleRemoveFavorite({type: "public_official"},official.id) 
                        : handleAddFavorite({type: "public_official"}, official.id)
                      }
                    >
                      {favoriteObjectIDs.includes(official.id) ? <IconStarFilled /> : <IconStar />}
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
                { <Group gap="xs" mb="xs">
                  <Text fw={700}>{t('social_media')}:</Text>
                  {Object.entries(official.social_media_handles).map(([platform, handle], index) => (
                    handle === null ? null :
                    <Badge
                      key={index}
                      leftSection={<SocialMediaIcon platform={platform} />}
                      variant="outline"
                    >
                      {handle}
                    </Badge>
                    
                  ))}
                </Group> }
                <Text mt="md" size="xs" c="dimmed">
                  {t('added_date')} {getDateFromObjectId(official.id).toLocaleDateString()}
                </Text>
              </Card>
            ))}
          </Stack>
        )}
      </ScrollArea>
    </Box>
  );
};