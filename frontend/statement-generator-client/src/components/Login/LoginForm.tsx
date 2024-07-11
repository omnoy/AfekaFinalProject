import { useForm } from '@mantine/form';
import { Text, TextInput, PasswordInput, Button, Group } from '@mantine/core';
import api from '../../services/api';
import { useState} from 'react';
import { useAuth } from '../../context/AuthProvider';
import { useNavigate } from 'react-router-dom';

interface LoginFormValues {
    email: string;
    password: string;
}


function LoginForm() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  
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
        const response = await api.post('/auth/login', values);
        if (response.status === 200) {
            login(response.data.user, 
                  response.data.user.role, 
                  response.data.access_token);
            console.log('Login successful:', response.data);
            navigate('/generate');
        }
        else if(response.status == 401){
            setError('Error' + response.data.error);
        }
    } catch (error: any) {
      console.error('Login failed:', error);
      if(error.response){
        setError('Error' + error.response.data.error);
      }
      else if(error.request){
        setError('Error: No response from server');
      }
      else {
        setError('Login failed, please try again');
      }
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
      <Text ta='center' mt='md' c='red'>
        {error}
      </Text>
    </form>
  );
}

export default LoginForm;