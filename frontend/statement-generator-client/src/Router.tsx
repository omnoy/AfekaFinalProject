import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home.page';
import { LoginPage } from './pages/Login.page';
import { RegisterPage } from './pages/Register.page';
import { PostGeneratorPage } from './pages/PostGenerator.page';
import { PostHistoryPage } from './pages/PostHistory.page';
import { UserProfilePage } from './pages/UserProfile.page';
import { NavigationHeader } from './components/NavigationHeader/NavigationHeader';
import { ErrorPage } from './pages/Error.page';
import { LogoutPage } from './pages/Logout.page';
import { PublicOfficialsPage } from './pages/PublicOfficials.page';
import AuthRedirector from './components/AuthComponents/AuthRedirector';

const router = createBrowserRouter([
  {
    path: '/',
    element: 
    <AuthRedirector type='public'>
      <HomePage />
    </AuthRedirector>
  },
  {
    path: '/login',
    element: 
    <AuthRedirector type='public'>
      <LoginPage />
    </AuthRedirector>
  },
  {
    path: '/register',
    element: 
    <AuthRedirector type='public'>
      <RegisterPage />
    </AuthRedirector>
  },
  {
    path: '/generate',
    element: 
    (
      <AuthRedirector type='private'>
        <NavigationHeader route='/generate'/>
        <PostGeneratorPage />
      </AuthRedirector>
    )
  },
  {
    path: '/history',
    element: 
    (
        <AuthRedirector type='private'>
          <NavigationHeader route='/history'/>
          <PostHistoryPage />
        </AuthRedirector>
    )
  },
  {
    path: '/profile',
    element: 
    (
      <AuthRedirector type='private'>
        <NavigationHeader route='/profile'/>
        <UserProfilePage />
      </AuthRedirector>
    )
  },
  {
    path: '/public-officials',
    element: 
    (
      <AuthRedirector type='private'>
        <NavigationHeader route='/public-officials'/>
        <PublicOfficialsPage />
      </AuthRedirector>
    )
  },
  {
    path: '/logout',
    element: 
    (
      <AuthRedirector type='private'>
        <NavigationHeader route='/logout'/>
        <LogoutPage />
      </AuthRedirector>
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
