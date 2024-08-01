import { render, screen, userEvent } from '../test-utils';
import  { HomePage }  from '../src/pages/Home.page';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import i18n from '@/services/i18n';
import { ChangeLanguageToggle } from '@/components/ChangeLanguageFooter/ChangeLanguageFooter';

describe('Home Page', () => {
  it('renders correctly', () => {
    render(
    <BrowserRouter>
      <I18nextProvider i18n={i18n}>
        <HomePage />
      </I18nextProvider>
    </BrowserRouter>
    );
    expect(screen.getByTestId('welcome-title')).toBeInTheDocument();
    expect(screen.getByTestId('instruction-text')).toBeInTheDocument();
    expect(screen.getByTestId('login-button')).toBeInTheDocument();
    expect(screen.getByTestId('register-button')).toBeInTheDocument();
});
  it('has correct links for login and register buttons', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <BrowserRouter>
          <HomePage />
        </BrowserRouter>
      </I18nextProvider>
    );

    expect(screen.getByTestId('login-link')).toHaveAttribute('href', '/login');
    expect(screen.getByTestId('register-link')).toHaveAttribute('href', '/register');
});
  it('correctly switches languages', async () => {
    render(
      <I18nextProvider i18n={i18n}>
        <BrowserRouter>
          <HomePage />
          <ChangeLanguageToggle />
        </BrowserRouter>
      </I18nextProvider>
    );
    
    expect(screen.getByTestId('welcome-title')).toHaveTextContent("Welcome to the Public Official Statement Generator.");
    expect(screen.getByTestId('instruction-text')).toHaveTextContent("To begin, please log in or register.");
    expect(screen.getByTestId('login-button')).toHaveTextContent("Login");
    expect(screen.getByTestId('register-button')).toHaveTextContent("Register");

    const toggleLanguageButton = screen.getByTestId('toggle-language-button');
    await userEvent.click(toggleLanguageButton);
    
    expect(screen.getByTestId('welcome-title')).toHaveTextContent("ברוך הבא למחולל המסרים עבור אנשי ציבור.");
    expect(screen.getByTestId('instruction-text')).toHaveTextContent("להתחיל, התחבר למשתמש קיים או צור משתמש.");
    expect(screen.getByTestId('login-button')).toHaveTextContent("התחברות למשתמש");
    expect(screen.getByTestId('register-button')).toHaveTextContent("צור משתמש");
    
    await userEvent.click(toggleLanguageButton);

    expect(screen.getByTestId('welcome-title')).toHaveTextContent("Welcome to the Public Official Statement Generator.");
    expect(screen.getByTestId('instruction-text')).toHaveTextContent("To begin, please log in or register.");
    expect(screen.getByTestId('login-button')).toHaveTextContent("Login");
    expect(screen.getByTestId('register-button')).toHaveTextContent("Register");
  });
});

