import  { useTranslation, } from 'react-i18next';
import  { US, IL } from 'country-flag-icons/react/3x2'
import { Group, useDirection } from '@mantine/core'
export const ChangeLanguageToggle = () => {
    const { i18n } = useTranslation();
    const { toggleDirection } = useDirection();
    const lang = i18n.language;

    const handleChangeLanguage = (lang: string) => {
        i18n.changeLanguage(lang);
        toggleDirection();
    };

    return (
        <>
            <Group justify='center' mt='xl'>
                {lang === 'eng' ?
                    <US onClick={() => handleChangeLanguage('heb')} height={40}/>
                :
                    <IL onClick={() => handleChangeLanguage('eng')} height={40}/>
                }
            </Group>
        </>
    );
}