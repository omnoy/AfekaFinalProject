import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home.page';
import { LoginPage } from './pages/Login.page';
import { RegisterPage } from './pages/Register.page';
import { PostGeneratorPage } from './pages/PostGenerator.page';
import { PostHistoryPage } from './pages/PostHistory.page';
import { UserProfilePage } from './pages/UserProfile.page';
import { NavigationHeader } from './components/NavigationHeader/NavigationHeader';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  {
    path: '/generate',
    element: 
    (
      <>
        <NavigationHeader route='/generate'/>
        <PostGeneratorPage />
      </>
    )
  },
  {
    path: '/history',
    element: 
    (
      <>
        <NavigationHeader route='/history'/>
        <PostHistoryPage />
      </>
    )
  },
  {
    path: '/profile',
    element: 
    (
      <>
        <NavigationHeader route='/profile'/>
        <UserProfilePage />
      </>
    )
  }
]);

export function Router() {
  return <RouterProvider router={router} />;
}
