import React, { useEffect, useState } from 'react';
import { Select, Textarea, Button, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import { GeneratedPost } from './GeneratedPost';
import { createAuthApi } from '@/services/api';
import { useAuth } from '@/context/AuthProvider';
import { useHttpError } from '@/hooks/useHttpError';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';

interface SocialMediaPostFormValues {
  public_official: string;
  prompt: string;
  social_media: string;
}

const socialMediaPlatforms = [
  { value: 'twitter', label: 'Twitter' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' },
  { value: 'linkedin', label: 'LinkedIn' },
];

export const PostGenerator: React.FC = () => {
    const [generatedPostTitle, setGeneratedPostTitle] = useState<string | null>(null);
    const [generatedPost, setGeneratedPost] = useState<string | null>(null);
    const { accessToken } = useAuth();
    const authApi = createAuthApi(accessToken);
    const {error, setError, handleError, clearError} = useHttpError();
    const { publicOfficials, loading, poError, refetch } = usePublicOfficials();
    
    const poDropDown = publicOfficials.map((official: any) => ({
        value: official.id,
        label: official.name_eng,
    }));
    
    const form = useForm<SocialMediaPostFormValues>({
    mode: 'uncontrolled',
    initialValues: {
        public_official: '',
        prompt: '',
        social_media: '',
    },
    validate: {
        public_official: (value) => (value ? null : 'Please select a public official'),
        prompt: (value) => (value ? null : 'Prompt cannot be empty'),
        social_media: (value) => (value ? null : 'Please select a social media platform'),
    },
    });

    const handleSubmit = async (values: SocialMediaPostFormValues) => {
        console.log('Form values:', values);
        const public_official = publicOfficials.find((official) => official.id === values.public_official);
        const post_generation_data = {
            public_official_id: public_official?.id,
            generation_prompt: values.prompt,
            social_media: values.social_media,
        };

        try {
            const response = await authApi.post('/post-generation/generate', post_generation_data);
            if (response.status === 200) {
                console.log('Post Generated: ', response.data);
                clearError();
                setGeneratedPostTitle(response.data.generated_post.title);
                setGeneratedPost(response.data.generated_post.text);
            }
            else {
                handleError(new Error('Unknown Error'));
            }

        } catch(error: any){ 
            handleError(error);
        }
    };

    return (
    <Box maw={400} mx="auto">
        <form onSubmit={form.onSubmit(handleSubmit)}>
        <Select
            label="Public Official"
            placeholder="Select a public official"
            data={poDropDown}
            {...form.getInputProps('public_official')}
        />
        <Textarea
            label="Prompt"
            placeholder="Enter your prompt here"
            minRows={4}
            autosize
            {...form.getInputProps('prompt')}
        />
        <Select
            label="Social Media Platform"
            placeholder="Select a social media platform"
            data={socialMediaPlatforms}
            {...form.getInputProps('social_media')}
        />
        <Button type="submit" mt="md">
            Generate Post
        </Button>
        </form>
        {error && <Box mt="md" c="red">{error}</Box>}
        {generatedPost && <GeneratedPost title={generatedPostTitle} post={generatedPost} />}
    </Box>
    );
};