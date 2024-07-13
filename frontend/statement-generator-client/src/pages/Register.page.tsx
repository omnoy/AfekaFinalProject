import { RegisterForm } from "@/components/Register/RegisterForm";
import { Text, Container, Title } from "@mantine/core";
import { Link } from "react-router-dom";

export function RegisterPage() { 
    return (
        <Container size="sm">
            <Title ta="center" mx='auto'>
                Register
            </Title>
            <RegisterForm />
            <Text ta="center" mt="xl">
                Already registered? <Link to="/login">Log in here.</Link>
            </Text>
        </Container>
    );
}