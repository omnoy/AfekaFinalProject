import React, { useState } from 'react';
import { Select, Textarea, Button, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import { GeneratedPost } from './GeneratedPost';

interface SocialMediaPostFormValues {
  public_official: string;
  prompt: string;
  social_media: string;
}

const publicOfficials = [
  { value: 'po_id_1', label: 'Benjamin Netanyahu' },
  { value: 'po_id_2', label: 'Ehud Olmert' },
  { value: 'po_id_3', label: 'Naftali Bennett' },
  // Add more officials as needed
];

const socialMediaPlatforms = [
  { value: 'twitter', label: 'Twitter' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' },
  { value: 'linkedin', label: 'LinkedIn' },
];

export const PostGenerator: React.FC = () => {
    const [generatedPost, setGeneratedPost] = useState<string | null>(null);

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

    const handleSubmit = (values: SocialMediaPostFormValues) => {
        console.log('Form values:', values);
        const post = `${values.public_official} says: "${values.prompt}" (Posted on ${values.social_media})`;
        setGeneratedPost(post);
    };

    return (
    <Box maw={400} mx="auto">
        <form onSubmit={form.onSubmit(handleSubmit)}>
        <Select
            label="Public Official"
            placeholder="Select a public official"
            data={publicOfficials}
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
        <GeneratedPost post={generatedPost} />
    </Box>
    );
};