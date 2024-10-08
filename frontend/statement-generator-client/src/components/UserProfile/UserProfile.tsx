import React, { useEffect, useState } from 'react';
import { Box, TextInput, Button, Title, Text, Group, MantineTheme, useMantineTheme, Stack } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from '../../context/AuthProvider';
import api, { createAuthApi } from '@/services/api';
import { useHttpError } from '@/hooks/useHttpError';
import { useTranslation } from 'react-i18next';
import { User } from '@/types/User';
import { use } from 'chai';
interface UserProfileForm {
  email: string;
  username: string;
  role: string;
}

export const UserProfileComponent: React.FC = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const { user, setUser, getAccessToken } = useAuth();
  const authApi = createAuthApi(getAccessToken());
  const { error, handleError, clearError, HTTPErrorComponent } = useHttpError();
  const { t } = useTranslation('user_forms');
  const theme = useMantineTheme();

  const userToUserProfileForm = (user: User): UserProfileForm => {
    return {
      email: user.email,
      username: user.username,
      role: user.role,
    };
  }

  const form = useForm<UserProfileForm>({
    initialValues: user ? userToUserProfileForm(user) : { email: '', username: '', role: '' },
    validate: {
      username: (value: string) => {
        if (value.length < 4) {
          return t('form.username_error_short');
        }
        else if (!/^[a-zA-Z0-9]+$/.test(value)) {
          return t('form.username_error_non_alpha');
        }
          return null;
        }
    },
  });

  const handleSubmit = async (values: UserProfileForm) => {
    try {
      const response = await authApi.put('/user/update', values);
      if (response.status === 200) {
          console.log('Updated Profile:', response.data);
          setUser(response.data.user);
          form.setValues(userToUserProfileForm(response.data.user as User));

          setIsEditing(false);
          clearError();
          setSuccessMessage(t('profile.update_success'));
          setTimeout(() => setSuccessMessage(''), 3000);
      }
      else {
          handleError(new Error('Unknown Error'));
      }
  } catch (error: any) {
    handleError(error);
  }
  };
  
  const getInputStyles = (theme: MantineTheme, editable: boolean) => ({
    input: {
      color: editable ? theme.colors.gray[9] : theme.colors.gray[6], 
      backgroundColor: theme.colors.gray[0], 
    },
  });

  return (
    <Box maw={400} mx="auto">
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack mt="md">
          <TextInput
          label={t('form.email')}
          {...form.getInputProps('email')}
          readOnly
          mb="md"
          styles={getInputStyles(theme, false)}
          />
          
          <TextInput
          label={t('form.role')}
          {...form.getInputProps('role')}
          readOnly
          mb="md"
          styles={getInputStyles(theme, false)}
          />
            
          <TextInput
          label={t('form.username')}
          {...form.getInputProps('username')}
          readOnly={!isEditing}
          mb="md"
          styles={getInputStyles(theme, isEditing)}
          />
            
        </Stack>

        {successMessage && (<Text c="teal" mb="md">{successMessage}</Text>)} 
        <HTTPErrorComponent />
        <Group justify="space-between" mt="xl">
          {!isEditing ? (
            <Button onClick={() => 
                {
                    setIsEditing(true); 
                    setSuccessMessage('');
                    clearError();
                }
            }>
            {t('profile.edit_button')}
            </Button>
          ) : (
            <>
              <Button type="submit" color="blue">{t('profile.save_changes_button')}</Button>
              <Button color="gray" onClick={() => 
                {
                    setIsEditing(false);
                    setSuccessMessage('');
                    clearError();
                }
            }>
                {t('profile.cancel_button')}
            </Button>
            </>
          )}
        </Group>
      </form>
    </Box>
  );
};