import React, { useEffect, useState } from 'react';
import { Box, Text, Card, Stack, Group, Badge, Title, Button, ScrollArea } from '@mantine/core';
import { useHttpError } from '@/hooks/useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { createAuthApi } from '@/services/api';
import { useTranslation } from 'react-i18next';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { useFavoriteObjects } from '@/hooks/useFavorites';
import { ObjectDisplayContainer } from '../ObjectDisplayContainer/ObjectDisplayContainer';
import { PublicOfficialCard } from './PublicOfficialCard';
import { use } from 'chai';
import { PublicOfficial } from '@/types/PublicOfficial';
import { g } from 'vitest/dist/suite-IbNSsUWN';
import { Link } from 'react-router-dom';

export const PublicOfficialsDisplay: React.FC = () => {
  
  const { publicOfficials, setPublicOfficials, loadingPublicOfficials, fetchPublicOfficials } = usePublicOfficials();
  const { accessToken } = useAuth();
  const authApi = createAuthApi(accessToken);
  const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
  const { t, i18n } = useTranslation('public_officials');
  const [displayedPublicOfficials, setDisplayedPublicOfficials] = useState<PublicOfficial[]>([]);
  const [publicOfficialsDisplayedType, setPublicOfficialsDisplayedType] = useState<'all' | 'favorites'>('all');
  const { getFavoriteObjectIDs, favoriteObjectIDs, handleAddFavorite, handleRemoveFavorite } = useFavoriteObjects();
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [publicOfficialsEmpty, setPublicOfficialsEmpty] = useState<boolean>(false);

  useEffect(() => {
    const getPublicOfficialsByType = async (type: 'all' | 'favorites') => {
      fetchPublicOfficials(type);
      console.log(publicOfficials);
      setDisplayedPublicOfficials(publicOfficials);
      if (sortDirection === 'asc'){
        const sortedPublicOfficials = displayedPublicOfficials.reverse();
        setDisplayedPublicOfficials([...sortedPublicOfficials]);
      }
    }
    getPublicOfficialsByType(publicOfficialsDisplayedType);
  }, [publicOfficialsDisplayedType]);

  useEffect(() => {
    getFavoriteObjectIDs({type: 'public_official'});
    console.log(publicOfficials)
    fetchPublicOfficials(publicOfficialsDisplayedType);
  }, []);

  useEffect(()=> {
    const sortPublicOfficials = () => {
      const sortedPosts = publicOfficials.reverse();
      setPublicOfficials([...sortedPosts]);
    }
    sortPublicOfficials();
  }, [sortDirection]);

  useEffect(() => {
    const checkPublicOfficialsEmpty = () => {
      if (!loadingPublicOfficials) {
        setPublicOfficialsEmpty(publicOfficials.length === 0);
      }
    }
    checkPublicOfficialsEmpty();
  }, [publicOfficials]);
    

  return (
    <Box p="md">
      <ObjectDisplayContainer objectsDisplayedType={publicOfficialsDisplayedType} setObjectsDisplayedType={setPublicOfficialsDisplayedType} sortDirection={sortDirection} setSortDirection={setSortDirection} />
      <HTTPErrorComponent />
      <ScrollArea h={600} type='always'>
        {loadingPublicOfficials ? (
          <Text>{t('loading')}</Text>

        ) : (
          <Stack gap="lg">
            {!loadingPublicOfficials && publicOfficialsEmpty ? 
              publicOfficialsDisplayedType === 'all' ?
              <Text>{t('no_public_officials_text')}</Text>
              :
              <Text>{t('no_favorites_text')}</Text>
            :
            publicOfficials.map((official) => (
              <PublicOfficialCard key={official.id} publicOfficial={official} favoriteObjectIDs={favoriteObjectIDs} handleAddFavorite={handleAddFavorite} handleRemoveFavorite={handleRemoveFavorite} />
            ))
          }
          </Stack>
        )}
      </ScrollArea>
    </Box>
  );
};