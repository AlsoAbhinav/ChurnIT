import React from 'react';
import './About.css';
import group from '../../assets/group.jpg';

const About = ({ isDarkMode }) => {
  const titleStyle = {
    color: isDarkMode ? '#00b4ff' : '#000f38'  // Bright blue in dark mode, dark blue in light mode
  };

  return (
    <div className='about'>
      <div className='about-left'>
        <img src={group} alt="" className='about-img'/>
      </div>
      
      <div className='about-right'>
        <h3>ABOUT US</h3>
        <h2 style={titleStyle}>Who We Are</h2>
        <p>Welcome to ChurnIT, your go-to solution for predicting and preventing customer churn. We specialize in providing businesses with the insights and tools needed to retain their most valuable asset—their customers.</p>
        <p>We offer advanced analytics, actionable insights, and customized solutions, all through a user-friendly platform. Our innovative technology and dedicated support ensure that you can easily access and implement our strategies to enhance customer retention.</p>
        <p>Choose ChurnIT for proven results and a customer-centric approach that prioritizes your business's success. Join us and transform the way you manage customer relationships for sustainable growth.</p>
      </div>
    </div>
  );
};

export default About;