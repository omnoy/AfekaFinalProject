import { Title, Text } from '@mantine/core';
import classes from './Welcome.module.css';

export function Welcome() {
  return (
    <>
      <Title className={classes.title} ta="center" mt={100}>
        Welcome to the Statement Generator
      </Title>
      <Text ta="center" size="lg" maw={580} mx="auto" mt="xl">
        To begin, please log in or register.
      </Text>
    </>
  );
}
