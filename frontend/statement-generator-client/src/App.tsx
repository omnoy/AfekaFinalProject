import '@mantine/core/styles.css';
import { DirectionProvider, MantineProvider } from '@mantine/core';
import { Router } from './Router';
import { theme } from './theme';
import React from 'react';
import { AuthProvider } from './context/AuthProvider';
import { I18nextProvider } from 'react-i18next';

import i18n from './services/i18n';
import { ChangeLanguageToggle } from './components/ChangeLanguageFooter/ChangeLanguageFooter';

export default function App() {
  return (
    <React.StrictMode>
      <MantineProvider theme={theme}>
        <I18nextProvider i18n={i18n}>
          <AuthProvider>
            <DirectionProvider>
              <Router />
              <ChangeLanguageToggle />
            </DirectionProvider>
          </AuthProvider>
        </I18nextProvider>
      </MantineProvider>
    </React.StrictMode>
  );
}
