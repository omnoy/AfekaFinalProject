import React, { createContext, useContext, useState, ReactNode } from 'react';
import { User } from '../types/User';
import Cookies from 'js-cookie';

interface AuthContextType {
  user: User | undefined;
  role: string | undefined;
  login: (user: User, role: string, accessToken: string) => void;
  logout: () => void;
  getAccessToken: () => string | undefined;
  updateUser: (user: User | undefined) => void;
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

  const login = (user: User, role: string, accessToken: string) => {
    console.log('Login successful:', user, role, accessToken);
    setUser(user);
    setRole(role);
    Cookies.set('accessToken', accessToken, { expires: 1, secure: true });
  };

  const logout = () => {
    setUser(undefined);
    setRole(undefined);
    Cookies.remove('accessToken');
  };

  const updateUser = (updatedUser: User | undefined) => {
    if (!updatedUser) {
      setUser(undefined);
      return;
    }
    setUser(updatedUser);
  }

  const getAccessToken = () => {
    return Cookies.get('accessToken');
  }

  const value = {
    user,
    role,
    getAccessToken,
    login,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};