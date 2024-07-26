// usePublicOfficials.ts
import { useState, useEffect } from 'react';
import { createAuthApi } from '@/services/api'; 
import { useHttpError } from './useHttpError';
import { useAuth } from '@/context/AuthProvider';
import { PublicOfficial } from '@/types/PublicOfficial';

export const usePublicOfficials = () => {
    const { accessToken } = useAuth();
    const authApi = createAuthApi(accessToken);
    const [publicOfficials, setPublicOfficials] = useState<PublicOfficial[]>([]);
    const [loading, setLoading] = useState(false);
    const { error, handleError, clearError } = useHttpError();
    const [poError, setPoError] = useState<string | null>('');

    const fetchPublicOfficials = async () => {
        setLoading(true);
        try {
            const response = await authApi.get('/public-official/all');
            if (response.status === 200) {
                console.log('Public Officials:', response.data);
                const officials = Array.from(response.data.public_officials) as PublicOfficial[];
                setPublicOfficials(officials);
            } else {
                handleError(new Error('Unknown Error loading Public Officials'));
            }
        } catch (error: any) {
            handleError(error);
        } finally {
            setLoading(false);
        }
        setPoError(error);
    };

    useEffect(() => {
        fetchPublicOfficials();
    }, [accessToken]);

    return { publicOfficials, loading, poError, refetch: fetchPublicOfficials };
    };