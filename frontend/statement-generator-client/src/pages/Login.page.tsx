import LoginForm from "@/components/Login/LoginForm";
import { Container, Text, Title } from "@mantine/core";

export function LoginPage() {
  return (
    <>
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Login
            </Title>
            <LoginForm />
            <Text ta="center" mt="xl">
                Don't have an account? <a href="/register">Register here.</a>
            </Text>
        </Container>
    </>
  );
}