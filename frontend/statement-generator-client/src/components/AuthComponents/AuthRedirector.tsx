import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthProvider";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { createAuthApi } from "@/services/api";
import { useHttpError } from "@/hooks/useHttpError";
import { bool } from "prop-types";
import { use } from "chai";
import { Center, Loader } from "@mantine/core";

interface AuthRedirectorProps {
    type: 'public' | 'private';
    children?: React.ReactNode;
}

const AuthRedirector: React.FC<AuthRedirectorProps> = ({type, children}) => {
    const { getAccessToken, isLoggedIn, setIsLoggedIn, accessTokenLogin, logout } = useAuth();
    const { handleError } = useHttpError();
    const [hasChecked, setHasChecked] = useState<boolean>(false);
    const location = useLocation();

    useEffect(() => {
        const checkUser = async () => {
            if (isLoggedIn) {
                setHasChecked(true);
            }
            else if (getAccessToken()) {
                if (!hasChecked) {
                    try {
                        const authApi = createAuthApi(getAccessToken());
                        const response = await authApi.get("user/get");
                        if (response.status === 200) {
                            console.log('User Profile Loaded:', response.data);
                            accessTokenLogin(response.data.user, response.data.user.role);
                        } else if (response.status === 401) {
                            logout();
                        } else {
                            handleError(new Error('Unknown Error Loading User Profile'));
                        }
                    } catch {
                        handleError(new Error('Unknown Error Loading User Profile'));
                    } finally {
                        setHasChecked(true);
                    }
                }
            } else {
                setHasChecked(true);
            }
        }

        checkUser();
    }, []);

    if (type === 'public') {
        return (
            isLoggedIn ? <Navigate to="/generate" state={{ from: location.pathname }} /> : 
                hasChecked ? children : <Center mt="xl"><Loader /></Center> 
            //if user is logged in, redirect to /generate page as homepage
        );
    }
    else {
        return (
            isLoggedIn ? children : 
                hasChecked ? <Navigate to="/login" state={{ from: location.pathname }} /> : <Center mt="xl"><Loader /></Center> 
            //if user is not logged in, redirect to /login page
        );
    }
}

export default AuthRedirector;