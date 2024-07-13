import LoginForm from "@/components/Login/LoginForm";
import { Container, Text, Title } from "@mantine/core";
import { Link } from "react-router-dom";

export function LoginPage() {
  return (
    <>
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Login
            </Title>
            <LoginForm />
            <Text ta="center" mt="xl">
                Don't have an account? <Link to="/register">Register here.</Link>
            </Text>
        </Container>
    </>
  );
}