import { UserProfileComponent } from "@/components/UserProfile/UserProfile";
import { Container, Title } from "@mantine/core";
import { useTranslation } from "react-i18next";

export function UserProfilePage(){
    const { t } = useTranslation('user_forms');
    return (
        <Container size="sm">
            <Title ta="center" mx='auto' mb="md">
                {t('profile.title')}
            </Title>
            <UserProfileComponent />
        </Container>
    );
}