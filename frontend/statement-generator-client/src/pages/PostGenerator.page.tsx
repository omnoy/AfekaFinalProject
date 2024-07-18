import { Title, Text, Container } from "@mantine/core";
import { PostGenerator } from "@/components/PostGenerator/PostGenerator";
import { useTranslation } from "react-i18next";

export function PostGeneratorPage() {
  const { t } = useTranslation('post_generator');
  return (
    <Container size="sm">
        <Title ta="center" mx='auto'>
            {t('post_generator.title')}
        </Title>
        <PostGenerator />
    </Container>
  );
}