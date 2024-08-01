import  { useTranslation, } from 'react-i18next';
import  { US, IL } from 'country-flag-icons/react/3x2'
import { Button, Group, useDirection } from '@mantine/core'
export const ChangeLanguageToggle = () => {
    const { t, i18n } = useTranslation("global");
    const { toggleDirection } = useDirection();
    const lang = i18n.language;

    const handleChangeLanguage = (lang: string) => {
        i18n.changeLanguage(lang);
        toggleDirection();
    };

    return (
        <>
            <Group justify='center' mt='xl'>
                <Button 
                    onClick={() => handleChangeLanguage(lang === 'eng' ? 'heb' : 'eng')}
                    leftSection={lang === 'eng' ? <US height={20} /> : <IL height={20} />} 
                    variant="outline"
                    color="gray"
                    data-testid='toggle-language-button'>
                    {lang === 'eng' ? t('language.english') : t('language.hebrew')}
                </Button>
            </Group>
        </>
    );
}