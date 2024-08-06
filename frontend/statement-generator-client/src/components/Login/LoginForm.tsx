import { useForm } from '@mantine/form';
import { Text, TextInput, PasswordInput, Button, Group } from '@mantine/core';
import api from '../../services/api';
import { useAuth } from '../../context/AuthProvider';
import { useNavigate } from 'react-router-dom';
import { useHttpError } from '@/hooks/useHttpError';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';

interface LoginFormValues {
    email: string;
    password: string;
}


function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const {error, setError, handleError, HTTPErrorComponent} = useHttpError(); 
  const {t, i18n} = useTranslation('user_forms');
  const [loginLoading, setLoginLoading] = useState<boolean>(false);
  
  const form = useForm<LoginFormValues>({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
      password: '',
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
    },
  });

  const handleSubmit = async (values: LoginFormValues) => {
    let timeoutId;
    try {
      timeoutId = setTimeout(() => {
        setLoginLoading(true);
      }, 200);

      const response = await api.post('/auth/login', values);
      if (response.status === 200) {
          login(response.data.user, 
                response.data.user.role, 
                response.data.access_token);
          console.log('Login successful:', response.data);
          navigate('/generate');
      }
      else{
        handleError(new Error('Unknown Error'))
      }
    } catch (error: any) {
      if (error.response?.status === 401) {
        setError(t('login.invalid_email_or_password'));
      }
      else {
        handleError(error);
      }
    }
    finally {
      clearTimeout(timeoutId);
      setLoginLoading(false);
    }
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit) }>
      <TextInput 
        dir={i18n.language === 'eng' ? 'ltr' : 'rtl'}
        withAsterisk
        label={t('form.email')}
        placeholder={t('form.email_placeholder')}
        key={form.key('email')}
        {...form.getInputProps('email')}
      />
      <PasswordInput 
        dir={i18n.language === 'eng' ? 'ltr' : 'rtl'}
        withAsterisk
        label={t('form.password')}
        placeholder={t('form.password_placeholder')}
        type="password"
        key={form.key('password')}
        {...form.getInputProps('password')}
      />
      <Group justify="flex-end" mt="md">
        <Button type="submit" loading={loginLoading}>{t('form.submit_button')}</Button>
      </Group>
      <HTTPErrorComponent />
    </form>
  );
}

export default LoginForm;