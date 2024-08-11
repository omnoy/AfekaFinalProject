import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home.page';
import { LoginPage } from './pages/Login.page';
import { RegisterPage } from './pages/Register.page';
import { PostGeneratorPage } from './pages/PostGenerator.page';
import { PostHistoryPage } from './pages/PostHistory.page';
import { UserProfilePage } from './pages/UserProfile.page';
import { NavigationHeader } from './components/NavigationHeader/NavigationHeader';
import { ErrorPage } from './pages/Error.page';
import RequireAuth from './components/RequireAuth/RequireAuth';
import { LogoutPage } from './pages/Logout.page';
import { PublicOfficialsPage } from './pages/PublicOfficials.page';

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
        <RequireAuth>
            <NavigationHeader route='/generate'/>
            <PostGeneratorPage />
        </RequireAuth>
    )
  },
  {
    path: '/history',
    element: 
    (
        <RequireAuth>
            <NavigationHeader route='/history'/>
            <PostHistoryPage />
        </RequireAuth>
    )
  },
  {
    path: '/profile',
    element: 
    (
      <RequireAuth>
        <NavigationHeader route='/profile'/>
        <UserProfilePage />
      </RequireAuth>
    )
  },
  {
    path: '/public-officials',
    element: 
    (
      <RequireAuth>
        <NavigationHeader route='/public-officials'/>
        <PublicOfficialsPage />
      </RequireAuth>
    )
  },
  {
    path: '/logout',
    element: 
    (
      <RequireAuth>
        <NavigationHeader route='/logout'/>
        <LogoutPage />
      </RequireAuth>
    )
  },
  {
    path: '*',
    element: <ErrorPage errorCode={404}/>,
  }
]);

export function Router() {
  return <RouterProvider router={router} />;
}
