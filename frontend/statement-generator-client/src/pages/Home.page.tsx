import { Title, Text, Anchor, Button, Group } from '@mantine/core';
import { Link } from 'react-router-dom';
export function HomePage() {
  return (
    <>
      <Title ta="center" mt={100}>
        Welcome to the Statement Generator
      </Title>
      <Text ta="center" size="lg" maw={580} mx="auto" mt="xl">
        To begin, please log in or register.
      </Text>
      <Group justify="center" mt="xl">
      <Link to="/login">
          <Button>
              Login
          </Button>
        </Link>
        <Link to="/register">
          <Button>
              Register
          </Button>
        </Link>
      </Group>
    </>
  );
}
