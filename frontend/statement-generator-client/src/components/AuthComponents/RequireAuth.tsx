import { useState } from "react";
import { useAuth } from "../../context/AuthProvider";
import { Navigate, Outlet, useLocation } from "react-router-dom";

const RequireAuth = ( {children} : any) => {
    const { getAccessToken } = useAuth();
    const location = useLocation();

    return (
        getAccessToken() ? children : <Navigate to="/login" state={{ from: location.pathname }} />
    );
}

export default RequireAuth;