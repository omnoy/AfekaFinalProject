import { Title, Text, Button, Group } from '@mantine/core';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ChangeLanguageToggle } from '@/components/ChangeLanguageFooter/ChangeLanguageFooter';

export function HomePage() {
  const { t, i18n } = useTranslation('home');
  return (
    <>
      <Title ta="center" mt={100} data-testid="welcome-title">
        {t('welcome')}
      </Title>
      <Text ta="center" size="lg" maw={580} mx="auto" mt="xl" data-testid="instruction-text">
        {t('instruction')}
      </Text>
      <Group justify="center" mt="xl">
      <Link to="/login" data-testid="login-link">
          <Button data-testid="login-button">
              {t('login_button')}
          </Button>
        </Link>
        <Link to="/register" data-testid="register-link">
          <Button data-testid="register-button">
              {t('register_button')}
          </Button>
        </Link>
      </Group>
    </>
  );
}
