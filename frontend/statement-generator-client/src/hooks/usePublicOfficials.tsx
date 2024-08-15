// usePublicOfficials.ts
import { useState } from 'react';
import { createAuthApi } from '@/services/api'; 
import { useHttpError } from './useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { PublicOfficial } from '@/types/PublicOfficial';

export const usePublicOfficials = () => {
    const { getAccessToken  } = useAuth();
    const authApi = createAuthApi(getAccessToken());
    const [publicOfficials, setPublicOfficials] = useState<PublicOfficial[]>([]);
    const [loadingPublicOfficials, setLoadingPublicOfficials] = useState(false);
    const { error, handleError, clearError } = useHttpError();
    const [poError, setPoError] = useState<string | null>('');

    const fetchPublicOfficials = async (type: 'all' | 'favorites') => {
        setLoadingPublicOfficials(true);
        try {
            var url = '';
            if (type === 'all') {
                url = '/public-official/all';
            }
            else if(type === 'favorites') {
                url = '/user/favorites/public_official';
            }
            const response = await authApi.get(url);
            if (response.status === 200) {
                console.log('Public Officials:', response.data);
                var officials: PublicOfficial[] = [];
                if (type === 'all') {
                    officials = Array.from(response.data.public_officials) as PublicOfficial[];
                }
                else if(type === 'favorites') {
                    officials = Array.from(response.data.favorites) as PublicOfficial[];
                }
                setPublicOfficials(officials);
            } else {
                handleError(new Error('Unknown Error loading Public Officials'));
            }
        } catch (error: any) {
            handleError(error);
        } finally {
            setLoadingPublicOfficials(false);
        }
        setPoError(error);
    };

    return { publicOfficials, setPublicOfficials, loadingPublicOfficials, poError, fetchPublicOfficials };
    };