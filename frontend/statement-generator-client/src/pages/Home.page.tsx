import { Title, Text, Anchor, Button, Group } from '@mantine/core';
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
      <Anchor href="/login">
          <Button>
              Login
          </Button>
        </Anchor>
        <Anchor href="/register">
          <Button>
              Register
          </Button>
        </Anchor>
      </Group>
    </>
  );
}
