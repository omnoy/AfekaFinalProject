import { RegisterButton } from '@/components/Register/RegisterButton';
import { Welcome } from '../components/Welcome/Welcome';
import { LoginButton } from '@/components/Login/LoginButton';
import { Group } from '@mantine/core';
export function HomePage() {
  return (
    <>
      <Welcome />
      <Group justify="center" mt="xl">
        <LoginButton />
        <RegisterButton />
      </Group>
    </>
  );
}
