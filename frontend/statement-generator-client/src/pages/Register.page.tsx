import { RegisterForm } from "@/components/Register/RegisterForm";
import { Text, Container, Title } from "@mantine/core";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

export function RegisterPage() { 
    const { t } = useTranslation("user_forms");
    return (
        <Container size="sm">
            <Title ta="center" mt={100} mx='auto'>
                {t("register.title")}
            </Title>
            <RegisterForm />
            <Text ta="center" mt="xl">
                {t("register.login_redirect_text")} <Link to="/login">{t('register.login_redirect_link')}</Link>
            </Text>
        </Container>
    );
}