import { PublicOfficial } from "@/types/PublicOfficial";
import { favoriteObjectType } from "@/hooks/useFavorites";
import { useTranslation } from "react-i18next";
import { Text, Card, Group, Badge, Button } from '@mantine/core';
import { IconStar, IconStarFilled, IconBrandFacebook, IconBrandTwitter, IconBrandInstagram, IconBrandLinkedin } from '@tabler/icons-react';
import { getDateFromObjectId } from "@/services/getDateFromObjectId";

const SocialMediaIcon: React.FC<{ platform: string }> = ({ platform }) => {
    switch (platform.toLowerCase()) {
      case 'facebook': return <IconBrandFacebook size={16} />;
      case 'twitter': return <IconBrandTwitter size={16} />;
      case 'instagram': return <IconBrandInstagram size={16} />;
      case 'linkedin': return <IconBrandLinkedin size={16} />;
      default: return null;
    }
};  

interface PublicOfficialCardProps {
    publicOfficial: PublicOfficial;
    favoriteObjectIDs: string[];
    handleAddFavorite: (type: favoriteObjectType, postId: string) => Promise<void>;
    handleRemoveFavorite: (type: favoriteObjectType, postId: string) => Promise<void>;
}

export const PublicOfficialCard: React.FC<PublicOfficialCardProps> = ({publicOfficial, favoriteObjectIDs, handleAddFavorite, handleRemoveFavorite}) => {
    const { t, i18n } = useTranslation('public_officials');
    
    return (
        <Card key={publicOfficial.id} shadow="sm" padding="lg" radius="md" withBorder>
                <Card.Section withBorder inheritPadding py="xs">
                  <Group justify="space-between">
                    <Text fw={500}>
                      {i18n.language === 'eng' ? publicOfficial.full_name.eng : publicOfficial.full_name.heb} ({i18n.language === 'eng' ? publicOfficial.full_name.heb : publicOfficial.full_name.eng})
                    </Text>
                    <Button
                      onClick={() => favoriteObjectIDs.includes(publicOfficial.id) 
                        ? handleRemoveFavorite({type: "public_official"},publicOfficial.id) 
                        : handleAddFavorite({type: "public_official"}, publicOfficial.id)
                      }
                    >
                      {favoriteObjectIDs.includes(publicOfficial.id) ? <IconStarFilled /> : <IconStar />}
                    </Button>
                  </Group>
                </Card.Section>

                <Text mt="md" mb="xs">
                  <Text span fw={700}>{t('position')}: </Text>
                  {i18n.language === 'eng' ? publicOfficial.position.eng : publicOfficial.position.heb}
                </Text>

                {publicOfficial.age !== null && (
                  <Text mb="xs">
                    <Text span fw={700}>{t('age')}: </Text>
                    {publicOfficial.age}
                  </Text>
                )}

                {publicOfficial.political_party !== null && (
                <Text mb="xs">
                  <Text span fw={700}>{t('political_party')}: </Text>
                  {i18n.language === 'eng' ? publicOfficial.political_party?.eng : publicOfficial.political_party?.heb}
                </Text>
                )}
                { <Group gap="xs" mb="xs">
                  <Text fw={700}>{t('social_media')}:</Text>
                  {Object.entries(publicOfficial.social_media_handles).map(([platform, handle], index) => (
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
                  {t('added_date')} {getDateFromObjectId(publicOfficial.id).toLocaleDateString()}
                </Text>
              </Card>
    );
}