// Contact.jsx
import React, { useState } from 'react';
import './Contact.css';
import msg from '../../assets/msg-icon.png';
import mail from '../../assets/mail-icon.png';
import phone from '../../assets/phone-icon.png';
import location from '../../assets/location-icon.png';
import web from '../../assets/web.png';

const Contact = ({ isDarkMode }) => {
  const [result, setResult] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    setResult("Sending....");
    const formData = new FormData(event.target);

    formData.append("access_key", "22378d9c-d70d-4f9d-9e3d-d9d81b7b3b3b");

    const response = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (data.success) {
      setResult("Form Submitted Successfully");
      event.target.reset();
    } else {
      console.log("Error", data);
      setResult(data.message);
    }
  };

  const textStyle = {
    color: isDarkMode ? '#00b4ff' : '#000f38'  // Bright blue in dark mode, dark blue in light mode
  };

  return (
    <div className='contact'>
      <div className="contact-col">
        <h3 className="highlight-text" style={textStyle}>
          Send Us a Message <img src={msg} alt="" />
        </h3>
        <p>We'd love to hear from you! Whether you have questions about our services, need support, or want to share feedback, our team at ChurnIT is here to help. Fill out the form below with your details and message, and we'll get back to you as soon as possible.</p>

        <ul>
          <li><img src={mail} alt="" />churnit@gmail.com</li>
          <li><img src={phone} alt="" />+977 9843967104</li>
          <li><img src={location} alt="" />Kalimati, Kathmandu</li>
          <li><img src={web} alt="" />www.churnit.com</li>
        </ul>
      </div>
      <div className="contact-col">
        <form onSubmit={onSubmit}>
          <label>Your Name</label>
          <input type="text" name='name' placeholder='Enter your name' required />
          <label>Phone No</label>
          <input type="tel" name='phone' placeholder='Enter your number' required />
          <label>Write your message here</label>
          <textarea name='message' rows="6" placeholder='Enter your message' required />
          <button type='submit' className='btn dark-btn'>Submit Now</button>
        </form>
        <span>{result}</span>
      </div>
    </div>
  );
};

export default Contact;

