import { useForm } from '@mantine/form';
import { TextInput, PasswordInput, Button, Group } from '@mantine/core';
import api from '../../services/api';

interface LoginFormValues {
    email: string;
    password: string;
}


function LoginForm() {
  const form = useForm<LoginFormValues>({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
      password: '',
    },
    validate: {
      email: (value: string) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value: string) => {
        if (value.length < 8) {
          return 'Password is too short';
        }
        if (!/^[a-zA-Z0-9]+$/.test(value)) {
          return 'Password must contain only alphanumeric characters';
        }
        return null;
      },
    },
  });

  const handleSubmit = async (values: LoginFormValues) => {
    try {
        window.location.href = '/generate';
        const response = await api.post('/login', values);
        console.log('Login successful:', response.data);
      // Handle successful login (e.g., save token, redirect user)
    } catch (error) {
      console.error('Login failed:', error);
      // Handle login error (e.g., show error message to user)
    }
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <TextInput
        withAsterisk
        label='Email | דוא"ל'
        placeholder="your@email.com"
        key={form.key('email')}
        {...form.getInputProps('email')}
      />
      <PasswordInput
        withAsterisk
        label="Password | סיסמא"
        placeholder="Your password"
        type="password"
        key={form.key('password')}
        {...form.getInputProps('password')}
      />
      <Group justify="flex-end" mt="md">
        <Button type="submit">Submit</Button>
      </Group>
    </form>
  );
}

export default LoginForm;