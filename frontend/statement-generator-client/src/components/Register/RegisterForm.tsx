import { useForm } from '@mantine/form';
import { Text, TextInput, PasswordInput, Button, Group, Box } from '@mantine/core';
import api from '../../services/api';
import { useAuth } from '@/context/AuthProvider';
import { useNavigate } from 'react-router-dom';
import { useHttpError } from '@/hooks/useHttpError';
import { useTranslation } from 'react-i18next';

interface RegisterFormValues {
    email: string;
    password: string;
    confirmPassword: string;
    username: string;
}

export const RegisterForm: React.FC = () => {
    const { login } = useAuth();
    const navigate = useNavigate();
    const { error, setError, handleError, HTTPErrorComponent } = useHttpError();
    const { t } = useTranslation('user_forms');

    const form = useForm<RegisterFormValues>({
        mode: 'uncontrolled',
        initialValues: {
            email: '',
            password: '',
            confirmPassword: '',
            username: '',
        },
        validate: {
            email: (value: string) => {
                if (!/^\S+@\S+$/.test(value)) {
                    return t('form.email_error');
                }
                return null;
            },
            password: (value: string) => {
                if (value.length < 8) {
                    return t('form.password_error_short');
                }
                if (!/^[a-zA-Z0-9]+$/.test(value)) {
                    return t('form.password_error_non_alpha');
                }
                return null;
            },
            confirmPassword: (value: string, values: { password: string }) => {
                if (value !== values.password) {
                    return t('form.password_error_no_match');
                }
                return null;
            },
            username: (value: string) => {
                if (value.length < 4) {
                    return t('form.username_error_short');
                }
                else if (!/^[a-zA-Z0-9]+$/.test(value)) {
                    return t('form.username_error_non_alpha');
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
                username: values.username
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
                    label={t('form.email')}
                    placeholder={t('form.email_placeholder')}
                    key={form.key('email')}
                    {...form.getInputProps('email')}
                />
                <PasswordInput
                    withAsterisk
                    label={t('form.password')}
                    placeholder={t('form.password_placeholder')}
                    type="password"
                    key={form.key('password')}
                    {...form.getInputProps('password')}
                />
                <PasswordInput
                    withAsterisk
                    label={t('form.confirm_password')}
                    placeholder={t('form.confirm_password_placeholder')}
                    type="password"
                    key={form.key('confirmPassword')}
                    {...form.getInputProps('confirmPassword')}
                />
                <TextInput
                    withAsterisk
                    label={t('form.username')}
                    placeholder={t('form.username_placeholder')}
                    key={form.key('username')}
                    {...form.getInputProps('username')}
                />
                <Group justify="flex-end" mt="md">
                    <Button type="submit">{t('form.submit_button')}</Button>
                </Group>
            </form>
            <HTTPErrorComponent />
        </Box>
    );
}