import LoginForm from "@/components/Login/LoginForm";
import { Container, Text, Title } from "@mantine/core";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next"

export function LoginPage() {
  const { t, i18n} = useTranslation('user_forms');
  return (
    <>
        <Container size="sm">
            <Title ta="center" mx='auto'>
                {t('login.title')}
            </Title>
            <LoginForm />
            <Text ta="center" mt="xl">
                {t('login.register_redirect_message')} <Link to="/register">{t('login.register_redirect_link')}</Link>
            </Text>
        </Container>
    </>
  );
}