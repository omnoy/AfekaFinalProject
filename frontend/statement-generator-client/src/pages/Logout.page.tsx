import { LogoutComponent } from "@/components/Logout/LogoutComponent";
import { Container, Title, Text } from "@mantine/core";

export function LogoutPage() {
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Logout
            </Title>
            <Text ta="center" mt="xl">
                Are you sure you want to log out?
            </Text>
            <LogoutComponent />
        </Container>
    );
}