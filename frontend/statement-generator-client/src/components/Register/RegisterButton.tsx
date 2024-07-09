import {Button} from '@mantine/core';

export function RegisterButton() {
    const handleClick = () => {
        console.log('Register button clicked');
        window.location.href = '/register';
    }
  
    return (
        <Button onClick={handleClick}>
            Register
        </Button>
    );
}

