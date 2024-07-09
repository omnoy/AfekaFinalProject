import { PostHistory } from "@/components/PostHistory/PostHistory";
import { Container, Title, Text } from "@mantine/core";

export function PostHistoryPage() {
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Post History
            </Title>
            <PostHistory />
        </Container>
    );
}