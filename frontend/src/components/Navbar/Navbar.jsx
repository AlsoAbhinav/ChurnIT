import React, { useEffect, useState } from 'react';
import './Navbar.css';
import logo from '../../assets/logo.png';
import { Link as ScrollLink } from 'react-scroll';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import DarkModeToggle from '../../DarkModeToggle';
import { Menu, User } from 'lucide-react';

const Navbar = ({ toggleDarkMode, isDarkMode }) => {
  const [sticky, setSticky] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const isHomePage = location.pathname === '/';

  useEffect(() => {
    const handleScroll = () => {
      setSticky(window.scrollY > 60);
    };
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const NavLink = ({ to, children }) => {
    const handleClick = () => {
      setMobileMenuOpen(false);
    };

    return (
      <ScrollLink 
        to={to} 
        smooth={true} 
        offset={to === 'hero' ? 0 : -300} 
        duration={500}
        onClick={handleClick}
      >
        {children}
      </ScrollLink>
    );
  };

  return (
    <nav className={`${sticky ? 'sticky' : 'transparent'}`}>
      <img src={logo} alt="Logo" className="logo" />
      <button 
        className="mobile-menu-btn"
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        aria-label="Toggle menu"
      >
        <Menu />
      </button>
      <ul className={`navbar-menu ${mobileMenuOpen ? 'active' : ''}`}>
        <li><NavLink to="hero">Home</NavLink></li>
        <li className="dropdown">
          <ScrollLink to="our-services" smooth={true} offset={-300} duration={500}>
            <a href="#">Services</a>
          </ScrollLink>
          <ul className="dropdown-menu">
            <li><NavLink to="service1">Churn Rate Predictor</NavLink></li>
            <li><NavLink to="service2">Insightful Statistics</NavLink></li>
            <li><NavLink to="service3">Retention Strategies</NavLink></li>
            <li><NavLink to="service5">Notification System</NavLink></li>
          </ul>
        </li>
        <li><NavLink to="about">About Us</NavLink></li>
        <li><NavLink to="testimonials">Testimonials</NavLink></li>
        <li><NavLink to="contact">Contact Us</NavLink></li>
        <li className="toggle-container">
          <DarkModeToggle toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode}/>
        </li>
        <li>
          <RouterLink to="/login" className="profile-icon-container">
            <User className="w-6 h-6" />
          </RouterLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;