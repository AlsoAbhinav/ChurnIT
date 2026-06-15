import React from 'react';
import { Sun, Moon } from 'lucide-react'; // Importing Sun and Moon icons

const DarkModeToggle = ({ toggleDarkMode, isDarkMode }) => {
  return (
    <div className="dark-mode-toggle" onClick={toggleDarkMode}>
      {isDarkMode ? (
        <Sun /> // Show Sun icon in dark mode
      ) : (
        <Moon /> // Show Moon icon in light mode
      )}
    </div>
  );
};

export default DarkModeToggle;
