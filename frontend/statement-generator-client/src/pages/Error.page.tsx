import { Title, Text, Anchor } from "@mantine/core";

export function ErrorPage({ errorCode, errorMessage }: { errorCode: number, errorMessage: string }) {
    return (
        <div>
            <Title ta='center'>{errorCode}</Title>
            <Text ta='center' mt='md'>{errorMessage}</Text>
            <Anchor href="/">
                <Text ta='center' mt='md'>Go back to home
                </Text>
            </Anchor>
        </div>
    )
}