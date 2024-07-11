import { useEffect } from "react";
import { useAuth } from "../../context/AuthProvider";
import { Navigate, Outlet, useLocation } from "react-router-dom";

const RequireAuth = ( {children} : any) => {
    const { user } = useAuth();
    const location = useLocation();

    useEffect(() => {
    console.log(user);
    }, [user]);
    return (
        user ? children : <Navigate to="/login" state={{ from: location.pathname }} />
    );
}

export default RequireAuth;