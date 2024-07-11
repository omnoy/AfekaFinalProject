import React, { useState } from 'react';
import { Box, TextInput, Button, Title, Text, Group, MantineTheme, useMantineTheme } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from '../../context/AuthProvider';
import api, { createAuthApi } from '@/services/api';
interface UserProfile {
  email: string;
  username: string;
  position: string;
  role: string;
}

export const UserProfileComponent: React.FC = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const { user, updateUser, accessToken } = useAuth();
  const authApi = createAuthApi(accessToken);
  
  const theme = useMantineTheme();

  const loadUserProfile = (user_data: UserProfile | null) => {
    return {
      email: user_data?.email || '',
      username: user_data?.username || '',
      position: user_data?.position || '',
      role: user_data?.role || '',
    };
  }

  const form = useForm<UserProfile>({
    initialValues: loadUserProfile(user),
    validate: {
      username: (value) => (value.length < 3 ? 'Username must have at least 3 characters' : null),
      position: (value) => (value.length < 2 ? 'Position must have at least 2 characters' : null),
    },
  });

  const handleSubmit = async (values: UserProfile) => {
    try {
      const response = await authApi.put('/user/update', values);
      if (response.status === 200) {
          console.log('Updated Profile:', response.data);
          updateUser(response.data.user);
          form.setValues(loadUserProfile(response.data.user));

          setIsEditing(false);
          setErrorMessage('');
          setSuccessMessage('Profile updated successfully!');
          setTimeout(() => setSuccessMessage(''), 3000);
      }
      else if(response.status == 400){
          console.log('Error' + response.data.error);
          setErrorMessage('Error: Invalid request');
      }
      else if(response.status == 401){
          console.log('Error' + response.data.error);
          setErrorMessage('Error: Unauthorized access');
      }
  } catch (error: any) {
    console.error('Profile Update failed:', error);
    if(error.response){
      if(error.response.status == 400){
        console.log('Error' + error.response.data.error);
        setErrorMessage('Error: Invalid request');
      }
      else if(error.response.status == 401){
          console.log('Error' + error.response.data.error);
          setErrorMessage('Error: Unauthorized access');
      }
      else {
        console.log('Error' + error.response.data.error);
        setErrorMessage('Error: Invalid request');
      }
    }
    else if(error.request){
      console.log('Error: No response from server' + error);
      setErrorMessage('Error: No response from server');
    }
    else {
      console.log('Login failed, please try again' + error);
      setErrorMessage('Error: Login failed, please try again');
    }
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
        <Group mt="md">
            <TextInput
            label="Email"
            {...form.getInputProps('email')}
            readOnly
            mb="md"
            styles={getInputStyles(theme, false)}
            />
            <TextInput
            label="Role"
            {...form.getInputProps('role')}
            readOnly
            mb="md"
            styles={getInputStyles(theme, false)}
            />
            
        </Group>
        <Group mt="md">
            <TextInput
            label="Username"
            {...form.getInputProps('username')}
            readOnly={!isEditing}
            mb="md"
            styles={getInputStyles(theme, isEditing)}
            />
            <TextInput
            label="Position"
            {...form.getInputProps('position')}
            readOnly={!isEditing}
            mb="md"
            styles={getInputStyles(theme, isEditing)}
            />
            
        </Group>

        {successMessage && (<Text c="teal" mb="md">{successMessage}</Text>)} 
        {errorMessage && (<Text c="red" mb="md">{errorMessage}</Text>)}

        <Group justify="space-between" mt="xl">
          {!isEditing ? (
            <Button onClick={() => 
                {
                    setIsEditing(true); 
                    setSuccessMessage('');
                    setErrorMessage('');
                }
            }>
            Edit Profile
            </Button>
          ) : (
            <>
              <Button type="submit" color="blue">Save Changes</Button>
              <Button color="gray" onClick={() => 
                {
                    setIsEditing(false);
                    setSuccessMessage('');
                    setErrorMessage('');
                }
            }>
                Cancel
            </Button>
            </>
          )}
        </Group>
      </form>
    </Box>
  );
};