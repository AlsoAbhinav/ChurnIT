import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GlobalStyle, lightTheme, darkTheme } from './GlobalStyle';
import Navbar from './components/Navbar/Navbar';
import Hero from './components/Hero/Hero';
import Programs from './components/Programs/Programs';
import Title from './components/Title/Title';
import About from './components/About/About';
import Testimonials from './components/Testimonials/Testimonials';
import Contact from './components/Contact/Contact';
import Footer from './components/Footer/Footer';
import LoginPage from './components/LoginPage/LoginPage';
import AuthPage from './components/AuthPage/AuthPage';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
    } else {
      setIsDarkMode(false);
    }
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode((prev) => {
      const newMode = !prev;
      localStorage.setItem('theme', newMode ? 'dark' : 'light');
      return newMode;
    });
  };

  const HomePage = () => (
    <>
      <Hero />
      <div className="container">
        <Title subTitle="Our services" title="What We Offer" isDarkMode={isDarkMode} />
      </div>
      <Programs />
      <div className="container">
        <About isDarkMode={isDarkMode} />
        <Title subTitle="TESTIMONIALS" title="What our Clients say" isDarkMode={isDarkMode} />
        <Testimonials />
        <Title subTitle="Contact Us" title="Get in Touch" isDarkMode={isDarkMode} />
        <Contact isDarkMode={isDarkMode} />
      </div>
      <Footer />
    </>
  );

  return (
    <Router>
      <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
        <GlobalStyle />
        <Navbar toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </ThemeProvider>
    </Router>
  );
};

export default App;