import React, { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  username: string;
  email: string;
  position: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  role: string | null;
  accessToken: string | null;
  login: (user: User, role: string, accessToken: string) => void;
  logout: () => void;
  updateUser: (user: User) => void;
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
  const [user, setUser] = useState<User | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const login = (user: User, role: string, accessToken: string) => {
    console.log('Login successful:', user, role, accessToken);
    setUser(user);
    setRole(role);
    setAccessToken(accessToken);
  };

  const logout = () => {
    setUser(null);
    setRole(null);
    setAccessToken(null);
  };

  const updateUser = (updatedUser: User) => {
    setUser(updatedUser);
  
  }

  const value = {
    user,
    role,
    accessToken,
    login,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};