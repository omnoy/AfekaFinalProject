import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { User } from '../types/User';
import Cookies from 'js-cookie';
import { useHttpError } from '@/hooks/useHttpError';
import { createAuthApi } from '@/services/api';

interface AuthContextType {
  user: User | undefined;
  role: string | undefined;
  isLoggedIn: boolean;
  login: (user: User, role: string, accessToken: string) => void;
  accessTokenLogin: (user: User, role: string) => void;
  logout: () => void;
  getAccessToken: () => string | undefined;
  setUser: (user: User | undefined) => void;
  setRole: (role: string | undefined) => void;
  setIsLoggedIn: (isLoggedIn: boolean) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | undefined>(undefined);
  const [role, setRole] = useState<string | undefined>(undefined);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  const login = (user: User, role: string, accessToken: string) => {
    console.log('Login successful:', user, role, accessToken);
    setUser(user);
    setRole(role);
    Cookies.set('accessToken', accessToken, { expires: 1, secure: true });
    setIsLoggedIn(true);
  };

  const accessTokenLogin = (user: User, role: string) => {
    //login when entering the app with an access token in cookies
    console.log('Login successful:', user, role);
    setUser(user);
    setRole(role);
    setIsLoggedIn(true);
  };

  const logout = () => {
    setUser(undefined);
    setRole(undefined);
    Cookies.remove('accessToken');
    setIsLoggedIn(false);
  };

  const getAccessToken = () => {
    return Cookies.get('accessToken');
  }

  const value = {
    user,
    role,
    isLoggedIn,
    getAccessToken,
    login,
    accessTokenLogin,
    logout,
    setUser,
    setRole,
    setIsLoggedIn,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};