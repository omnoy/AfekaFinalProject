import { UserProfileComponent } from "@/components/UserProfile/UserProfile";
import { Container, Group, Title } from "@mantine/core";

export function UserProfilePage(){
    return (
        <Container size="sm">
            <Title ta="center" mx='auto' mb="md">
                User Profile
            </Title>
            <UserProfileComponent />
        </Container>
    );
}