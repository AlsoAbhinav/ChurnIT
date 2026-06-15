import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Hero.css';
import dark_arrow from '../../assets/dark-arrow.png';

const Hero = () => {
  const navigate = useNavigate();

  const handleGetStartedClick = () => {
    navigate('/login'); // Redirect to the login page
  };

  const text = "Keep your customers close    and your churn rate low with ChurnIT!";

  return (
    <div className='hero container'>
      <div className='herotext'>
        <h1 className="typewriter-text">
          {text.split("").map((letter, index) => (
            <span
              key={index}
              style={{ animationDelay: `${index * 0.07}s` }}
              className="animated-letter"
            >
              {letter === " " ? "\u00A0" : letter}
            </span>
          ))}
        </h1>
        <p>Predict and prevent customer attrition with our advanced churn prediction platform. Gain actionable insights, enhance customer retention strategies, and drive growth by understanding patterns and factors influencing customer churn.</p>
        <button className='btn' onClick={handleGetStartedClick}>
          Get Started
          <img src={dark_arrow} alt="" />
        </button>
      </div>
    </div>
  );
}

export default Hero;
