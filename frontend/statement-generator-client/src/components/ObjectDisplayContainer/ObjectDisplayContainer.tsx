
import { Box, Text, Card, Stack, Group, Badge, Title, Button, Anchor, NavLink, Loader, ScrollArea } from '@mantine/core';
import { useTranslation } from 'react-i18next';
import { IconArrowUp , IconArrowDown  } from '@tabler/icons-react';

interface ObjectDisplayContainerProps{ 
    objectsDisplayedType: 'all' | 'favorites';
    setObjectsDisplayedType: (type: 'all' | 'favorites') => void;
    sortDirection: 'asc' | 'desc';
    setSortDirection: (direction: 'asc' | 'desc') => void;
}

export const ObjectDisplayContainer: React.FC<ObjectDisplayContainerProps> = ({objectsDisplayedType, setObjectsDisplayedType, sortDirection, setSortDirection}) => {
    const { t } = useTranslation('global');

    return (
    <Group justify="space-between" mb='md'>
        <Button onClick={() => {setObjectsDisplayedType('all');}} variant='subtle'>
          <Title order={4} c={objectsDisplayedType === 'all' ? 'blue' : 'dimmed'}>{t('object_display_container.all')}</Title>
        </Button>
        
        <Button onClick={() => {setObjectsDisplayedType('favorites');}} variant='subtle'>
          <Title order={4} c={objectsDisplayedType === 'favorites' ? 'blue' : 'dimmed'}>{t('object_display_container.favorites')}</Title>
        </Button>

        <Button 
          onClick={() => setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')} 
          rightSection={sortDirection === 'asc' ? <IconArrowUp stroke={2}/> : <IconArrowDown stroke={2}/>}
          w={150}
          variant='subtle'
        >
          <Text>{t(`object_display_container.sort_${sortDirection}`)}</Text>
        </Button>
      </Group>
    );
}