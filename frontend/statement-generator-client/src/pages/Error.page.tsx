import { Title, Text, Anchor } from "@mantine/core";
import { useTranslation } from "react-i18next";

export function ErrorPage({ errorCode }: { errorCode: number }) {
    const { t } = useTranslation('global');
    return (
        <div>
            <Title ta='center' mt={100}>{errorCode}</Title>
            <Text ta='center' mt='md'>{t(`error.${errorCode}_error_text`)}</Text>
            <Anchor href="/">
                <Text ta='center' mt='md'>{t('error.return_home')}
                </Text>
            </Anchor>
        </div>
    )
}