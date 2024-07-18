import { PostHistory } from "@/components/PostHistory/PostHistory";
import { Container, ScrollArea, Title } from "@mantine/core";
import { useTranslation } from "react-i18next";

export function PostHistoryPage() {
    const { t } = useTranslation('post_generator');
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                {t('post_history.title')}
            </Title>
            <PostHistory />
        </Container>
    );
}