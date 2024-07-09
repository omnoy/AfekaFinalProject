import {Button} from '@mantine/core';

export function LoginButton() {
    const handleClick = () => {
        console.log('Login button clicked');
        window.location.href = '/login';
    }
  
    return (
        <Button onClick={handleClick}>
            Log In
        </Button>
    );
}

