import { useForm } from '@mantine/form';
import { TextInput, PasswordInput, Button, Group, Box } from '@mantine/core';
import api from '../../services/api';
import { useAuth } from '@/context/AuthProvider';
import { useNavigate } from 'react-router-dom';
import { useHttpError } from '@/hooks/useHttpError';

interface RegisterFormValues {
    email: string;
    password: string;
    confirmPassword: string;
    username: string;
    position: string;
}

export const RegisterForm: React.FC = () => {
    const { login } = useAuth();
    const navigate = useNavigate();
    const { error, setError, handleError } = useHttpError();


    const form = useForm<RegisterFormValues>({
        mode: 'uncontrolled',
        initialValues: {
            email: '',
            password: '',
            confirmPassword: '',
            username: '',
            position: '',
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
            confirmPassword: (value: string, values: { password: string }) => {
                if (value !== values.password) {
                    return 'Passwords do not match';
                }
                return null;
            },
            username: (value: string) => {
                if (value.trim() === '') {
                    return 'Username is required';
                }
                return null;
            },
            position: (value: string) => {
                if (value.trim() === '') {
                    return 'Position is required';
                }
                return null;
            },
        },
    });

    const handleSubmit = async (values: RegisterFormValues) => {
        try {
            const register_values = {
                email: values.email,
                password: values.password,
                username: values.username,
                position: values.position
            }

            const response = await api.post('auth/register', register_values);
            console.log('Registration successful:', response.data);
            if (response.status === 200) {
                login(response.data.user, 
                        response.data.user.role, response.data.access_token);
                navigate('/generate');
            }
            else {
                handleError(new Error('Unknown Error'));
            }
        } catch (error) {
            handleError(new Error('Unknown Error'));
        }
    };

    return (
        <Box maw={400} mx="auto">
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
                <PasswordInput
                    withAsterisk
                    label="Confirm Password | אשר סיסמא"
                    placeholder="Confirm your password"
                    type="password"
                    key={form.key('confirmPassword')}
                    {...form.getInputProps('confirmPassword')}
                />
                <TextInput
                    withAsterisk
                    label="Username | שם משתמש"
                    placeholder="Your username"
                    key={form.key('username')}
                    {...form.getInputProps('username')}
                />
                <TextInput
                    withAsterisk
                    label="Position | תפקיד"
                    placeholder="Your position"
                    key={form.key('position')}
                    {...form.getInputProps('position')}
                />
                <Group justify="flex-end" mt="md">
                    <Button type="submit">Submit</Button>
                </Group>
            </form>
        </Box>
    );
}