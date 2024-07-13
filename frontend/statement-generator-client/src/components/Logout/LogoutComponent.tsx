import { useAuth } from "@/context/AuthProvider";
import { useHttpError } from "@/hooks/useHttpError";
import { createAuthApi } from "@/services/api";
import { Button, Group, Text } from "@mantine/core";
import { useNavigate } from "react-router-dom";

export const LogoutComponent: React.FC = () => {
    const navigate = useNavigate();
    const { accessToken, logout } = useAuth();
    const authApi = createAuthApi(accessToken);
    const { error, handleError, clearError } = useHttpError();

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
        <Group justify="center" mt="xl">
            <Button onClick={() => handleLogout()} color="blue" variant="light">
                Logout
            </Button>
            {error && (<Text c="red" mb="md">{error}</Text>)}
        </Group>
    )
}