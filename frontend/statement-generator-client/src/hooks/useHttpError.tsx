import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Text } from '@mantine/core';
import { useAuth } from '@/context/AuthProvider';

export const useHttpError = () => {
  const [error, setError] = useState<string | null>(null);
  const [redirectTimer, setRedirectTimer] = useState<NodeJS.Timeout | null>(null);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleError = async (error: any) => {

    if (error.response) {
      switch (error.response.status) {
        case 400:
          setError('Error: Invalid request');
          break;
        case 401:
          error.response.data.msg === 'Token has expired' ? 
            setError('Error: Timed out. Please log in again.')
          :
            setError('Error: Unauthorized access');
          
          const timer = setTimeout(() => {
            logout();
            navigate('/login');
          }, 1000);

          setRedirectTimer(timer);
          break;
        case 500:
            setError('Error: Internal server error');
            break;
        default:
          setError(`Error ${error.response.status}: ${error.response.data.error || 'An error occurred'}`);
      }
    } else if (error.request) {
      setError('Error: No response from server');
    } else {
      setError('An unexpected error occurred. Please try again.');
    }
    console.error('Error details:', error);
  };

  const clearError = () => {
    setError(null);
    // Clear the redirect timer if it exists
    if (redirectTimer) {
      clearTimeout(redirectTimer);
      setRedirectTimer(null);
    }
  };

  // Clean up the timer if the component unmounts
  useEffect(() => {
    return () => {
      if (redirectTimer) {
        clearTimeout(redirectTimer);
      }
    };
  }, [redirectTimer]);

  const HTTPErrorComponent = () => (
    error ? <Text c="red" mb="md">{error}</Text> : null
  );

  return { error, setError, handleError, clearError, HTTPErrorComponent };
};