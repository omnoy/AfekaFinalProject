import { LogoutComponent } from "@/components/Logout/LogoutComponent";
import { Container, Title, Text } from "@mantine/core";
import { useTranslation } from "react-i18next";

export function LogoutPage() {
    const { t } = useTranslation('logout');
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                {t('title')}
            </Title>
            <Text ta="center" mt="xl">
                {t('validation')}
            </Text>
            <LogoutComponent />
        </Container>
    );
}