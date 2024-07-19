import React, { useEffect, useState } from 'react';
import { Text, Loader, Select, Textarea, Button, Box, Group, Stack } from '@mantine/core';
import { useForm } from '@mantine/form';
import { GeneratedPost } from './GeneratedPost';
import { createAuthApi } from '@/services/api';
import { useAuth } from '@/context/AuthProvider';
import { useHttpError } from '@/hooks/useHttpError';
import { usePublicOfficials } from '@/hooks/usePublicOfficials';
import { useTranslation } from 'react-i18next';
import { useForceUpdate } from '@mantine/hooks';

interface SocialMediaPostFormValues {
  public_official: string;
  prompt: string;
  social_media: string;
  language: string;
}

export const PostGenerator: React.FC = () => {
    const [generatedPostTitle, setGeneratedPostTitle] = useState<string | null>(null);
    const [generatedPostText, setGeneratedPostText] = useState<string | null>(null);
    const [generatedPostLanguage, setGeneratedPostLanguage] = useState<string | null>(null);
    const [generatedPostID, setGeneratedPostID] = useState<string>('');
    const { accessToken } = useAuth();
    const authApi = createAuthApi(accessToken);
    const {error, setError, handleError, clearError, HTTPErrorComponent} = useHttpError();
    const { publicOfficials, loading, poError, refetch } = usePublicOfficials();
    const [postLoading, setPostLoading] = useState<boolean>(false);
    const { t, i18n } = useTranslation('post_generator');

    const socialMediaPlatforms = [
        { value: 'twitter', label: t('social_media.twitter')},
        { value: 'facebook', label: t('social_media.facebook')},
        { value: 'instagram', label: t('social_media.instagram')},
        { value: 'linkedin', label: t('social_media.linkedin')},
      ];

    const languageDropdown = [
        { value: 'eng', label: t('languages.english')},
        { value: 'heb', label: t('languages.hebrew')},
    ];
    
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
            language: i18n.language
        },
        validate: {
            public_official: (value) => (value ? null : t('post_generator.public_official_error')),
            prompt: (value) => (value ? null : t('post_generator.prompt_error')),
            social_media: (value) => (value ? null : t('post_generator.social_media_error')),
            language: (value) => (value ? null : t('post_generator.language_error')),
        },
    });

    // useEffect(() => {
    //     form.setFieldValue('language', i18n.language);
    //   }, [i18n.language]);
    
    const handleSubmit = async (values: SocialMediaPostFormValues) => {
        clearError();
        setPostLoading(true);
        setGeneratedPostTitle(null);
        setGeneratedPostText(null);
        setGeneratedPostLanguage(null);
        console.log('Form values:', values);
        const public_official = publicOfficials.find((official) => official.id === values.public_official);
        const post_generation_data = {
            public_official_id: public_official?.id,
            generation_prompt: values.prompt,
            social_media: values.social_media,
            language: values.language,
        };

        try {
            const response = await authApi.post('/post-generation/generate', post_generation_data);
            if (response.status === 200) {
                console.log('Post Generated: ', response.data);
                setGeneratedPostTitle(response.data.generated_post.title);
                setGeneratedPostText(response.data.generated_post.text);
                setGeneratedPostLanguage(response.data.generated_post.language);
                setGeneratedPostID(response.data.generated_post.id);
            }
            else {
                handleError(new Error('Unknown Error'));
            }

        } catch(error: any){ 
            handleError(error);
        }
        finally
        {
            setPostLoading(false);
        }
    };

    return (
    <Box maw={800} mx="auto">
        <form onSubmit={form.onSubmit(handleSubmit)}>
            <Group gap="sm" mt="md" justify='space-between'>
                <Select
                    label={t('generated_post.public_official')}
                    placeholder={t('post_generator.public_official_placeholder')}
                    data={poDropDown}
                    searchable
                    nothingFoundMessage={t('post_generator.nothing_found')}
                    {...form.getInputProps('public_official')}
                />
                <Select
                    label={t('generated_post.social_media')}
                    placeholder={t('post_generator.social_media_placeholder')}
                    data={socialMediaPlatforms}
                    {...form.getInputProps('social_media')}
                />
                <Select
                    label={t('generated_post.language')}
                    placeholder={t('post_generator.language_placeholder')}
                    data={languageDropdown}
                    {...form.getInputProps('language')}
                />
            </Group>
            <Textarea
                label={t('generated_post.prompt')}
                placeholder={t('post_generator.prompt_placeholder')}
                mt='md'
                minRows={4}
                autosize
                {...form.getInputProps('prompt')}
            />
            
            <Button type="submit" mt="md" mb="md">
                {t('post_generator.generate_post_button')}
            </Button>
        </form>
        <HTTPErrorComponent />
        {postLoading ? 
        <Stack align='center' gap='md' justify='center'>
            <Text mt="md">{t('post_generator.generation_loading')}.</Text>
            <Loader mt="md" c='blue' type='bars'/>
        </Stack>
        : <GeneratedPost title={generatedPostTitle} post={generatedPostText} language={generatedPostLanguage} id={generatedPostID}/>
        }
        
    </Box>
    );
};