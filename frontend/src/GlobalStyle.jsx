import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${({ theme }) => theme.body};
    color: ${({ theme }) => theme.text};
  }
`;

export const lightTheme = {
  body: '#FFF',
  text: '#000'
};

export const darkTheme = {
  body: '#000',
  text: '#FFF'
};