import { PublicOfficialsDisplay } from "@/components/PublicOfficials/PublicOfficialDisplay";
import { Container, Title } from "@mantine/core";
import { useTranslation } from "react-i18next";

export function PublicOfficialsPage() {
    const { t } = useTranslation('public_officials');
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                {t('title')}
            </Title>
            <PublicOfficialsDisplay />
        </Container>
    );
}