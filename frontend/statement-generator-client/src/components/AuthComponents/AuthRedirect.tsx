import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthProvider";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { createAuthApi } from "@/services/api";
import { useHttpError } from "@/hooks/useHttpError";
import { bool } from "prop-types";
import { use } from "chai";

const AuthRedirector = ( {children} : any) => {
    const { getAccessToken, user, setUser, role, setRole, logout } = useAuth();
    const { handleError } = useHttpError();
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const location = useLocation();

    useEffect(() => {
        const checkUser = async () => {
            if (getAccessToken()) {
                try {
                    const authApi = createAuthApi(getAccessToken());
                    const response = await authApi.get("user/get");
                    if (response.status === 200) {
                        console.log('User Profile Loaded:', response.data);
                        setUser(response.data.user);
                        setRole(response.data.user.role);
                    } else if (response.status === 401) {
                        logout();
                    } else {
                        handleError(new Error('Unknown Error Loading User Profile'));
                    }
                } catch {
                    handleError(new Error('Unknown Error Loading User Profile'));
                }
            }
        }

        checkUser();
    }, []);

    useEffect(() => {
        if (user && role) {
            setIsLoggedIn(true);
        }
    }, [user, role]);

    return (
        isLoggedIn ? <Navigate to="/generate" state={{ from: location.pathname }} /> : children 
        //if user is logged in, redirect to /generate page as homepage
    );
}

export default AuthRedirector;