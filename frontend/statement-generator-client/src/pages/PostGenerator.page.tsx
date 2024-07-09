import { Title, Text, Container } from "@mantine/core";
import { PostGenerator } from "@/components/PostGenerator/PostGenerator";

export function PostGeneratorPage() {
  return (
    <Container size="sm">
        <Title ta="center" mx='auto'>
            Generate a Post | ייצר פוסט
        </Title>
        <PostGenerator />
    </Container>
  );
}