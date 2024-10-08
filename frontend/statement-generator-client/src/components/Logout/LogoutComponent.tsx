import { useAuth } from "@/context/AuthProvider";
import { useHttpError } from "@/hooks/useHttpError";
import { createAuthApi } from "@/services/api";
import { Button, Center, Group, Text } from "@mantine/core";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

export const LogoutComponent: React.FC = () => {
    const navigate = useNavigate();
    const { getAccessToken, logout } = useAuth();
    const authApi = createAuthApi(getAccessToken());
    const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
    const { t } = useTranslation('logout');

    const handleLogout = async () => {
        try {
            const response = await authApi.post('/auth/logout');
            if (response.status === 200){
                console.log('Logged out');
                logout();
                navigate('/');
            }
            else {
                handleError(new Error('Unknown Error'));
            }
            
        } catch(error: any) {
            handleError(error);
        }
        
    }

    return (
        <>
            <Center>
                <Button onClick={() => handleLogout()} color="blue" variant="light" mt="xl" mb="xl">
                    {t('logout_button')}
                </Button>
            </Center>
            <Center>
                <HTTPErrorComponent />
            </Center>
        </>
    )
}