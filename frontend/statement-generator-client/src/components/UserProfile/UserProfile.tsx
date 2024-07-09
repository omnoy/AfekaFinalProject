import React, { useState } from 'react';
import { Box, TextInput, Button, Title, Text, Group, MantineTheme, useMantineTheme } from '@mantine/core';
import { useForm } from '@mantine/form';

interface UserProfile {
  email: string;
  username: string;
  position: string;
  role: string;
}

const initialUserProfile: UserProfile = {
  email: 'user@example.com',
  username: 'johndoe',
  position: 'Software Developer',
  role: 'User',
};

export const UserProfileComponent: React.FC = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const theme = useMantineTheme();

  const form = useForm<UserProfile>({
    initialValues: initialUserProfile,
    validate: {
      username: (value) => (value.length < 3 ? 'Username must have at least 3 characters' : null),
      position: (value) => (value.length < 2 ? 'Position must have at least 2 characters' : null),
    },
  });

  const handleSubmit = (values: UserProfile) => {
    console.log('Updated profile:', values);
    setIsEditing(false);
    setSuccessMessage('Profile updated successfully!');
    setTimeout(() => setSuccessMessage(''), 3000);
  };
  
  const getInputStyles = (theme: MantineTheme, editable: boolean) => ({
    input: {
      color: editable ? theme.colors.gray[9] : theme.colors.gray[6], // Blue for editable, Gray for non-editable
      backgroundColor: theme.colors.gray[0], // White for editable, Light gray for non-editable
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
            label="Username"
            {...form.getInputProps('username')}
            readOnly={!isEditing}
            mb="md"
            styles={getInputStyles(theme, isEditing)}
            />
        </Group>
        <Group mt="md">
            <TextInput
            label="Position"
            {...form.getInputProps('position')}
            readOnly={!isEditing}
            mb="md"
            styles={getInputStyles(theme, isEditing)}
            />
            <TextInput
            label="Role"
            {...form.getInputProps('role')}
            readOnly
            mb="md"
            styles={getInputStyles(theme, false)}
            />
        </Group>

        {successMessage && (
          <Text color="teal" mb="md">{successMessage}</Text>
        )}

        <Group justify="space-between" mt="xl">
          {!isEditing ? (
            <Button onClick={() => 
                {
                    setIsEditing(true); 
                    setSuccessMessage('');
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