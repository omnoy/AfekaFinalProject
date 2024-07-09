import { RegisterForm } from "@/components/Register/RegisterForm";
import { Text, Container, Title } from "@mantine/core";

export function RegisterPage() { 
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Register
            </Title>
            <RegisterForm />
            <Text ta="center" mt="xl">
                Already registered? <a href="/register">Log in here.</a>
            </Text>
        </Container>
    );
}