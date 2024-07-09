import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { Router } from './Router';
import { theme } from './theme';
import React from 'react';

export default function App() {
  return (
    <React.StrictMode>
      <MantineProvider theme={theme}>
        <Router />
      </MantineProvider>
    </React.StrictMode>
  );
}
