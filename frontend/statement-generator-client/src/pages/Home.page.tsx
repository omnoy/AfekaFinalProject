import { Title, Text, Button, Group } from '@mantine/core';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ChangeLanguageToggle } from '@/components/ChangeLanguageFooter/ChangeLanguageFooter';

export function HomePage() {
  const { t, i18n } = useTranslation('home');
  return (
    <>
      <Title ta="center" mt={100}>
        {t('welcome')}
      </Title>
      <Text ta="center" size="lg" maw={580} mx="auto" mt="xl">
        {t('instruction')}
      </Text>
      <Group justify="center" mt="xl">
      <Link to="/login">
          <Button>
              {t('login_button')}
          </Button>
        </Link>
        <Link to="/register">
          <Button>
              {t('register_button')}
          </Button>
        </Link>
      </Group>
    </>
  );
}
