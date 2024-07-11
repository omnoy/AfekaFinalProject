import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { Router } from './Router';
import { theme } from './theme';
import React from 'react';
import { AuthProvider } from './context/AuthProvider';

export default function App() {
  return (
    <React.StrictMode>
      <MantineProvider theme={theme}>
        <AuthProvider>
          <Router />
        </AuthProvider>
      </MantineProvider>
    </React.StrictMode>
  );
}
