import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const useHttpError = () => {
  const [error, setError] = useState<string | null>(null);
  const [redirectTimer, setRedirectTimer] = useState<NodeJS.Timeout | null>(null);
  const navigate = useNavigate();

  const handleError = (error: any) => {

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
            navigate('/login');
          }, 3000);

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

  return { error, setError, handleError, clearError };
};