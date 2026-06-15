import React from 'react';
import './Title.css';

const Title = ({ subTitle, title, isDarkMode }) => {
  const titleStyle = {
    color: isDarkMode ? '#00b4ff' : '#000f38'  // Bright blue in dark mode, dark blue in light mode
  };

  return (
    <div className='title'>
      <p>{subTitle}</p>
      <h2 style={titleStyle}>{title}</h2>
    </div>
  );
};

export default Title;