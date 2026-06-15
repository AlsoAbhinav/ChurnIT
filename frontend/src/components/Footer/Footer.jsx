import React, { useState } from 'react';
import './Footer.css';

const Footer = () => {
  const [showTerms, setShowTerms] = useState(false);
  const [showPrivacy, setShowPrivacy] = useState(false);

  const Modal = ({ show, onClose, title, children }) => {
    if (!show) return null;

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <div className="modal-header">
            <h2>{title}</h2>
            <button onClick={onClose} className="close-button">&times;</button>
          </div>
          <div className="modal-body">
            {children}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className='footer'>
      <p>@ 2024-2025 ChurnIT. All rights reserved.</p>
      <ul>
        <li>
          <button className="footer-link" onClick={() => setShowTerms(true)}>
            Terms of Services
          </button>
        </li>
        <li>
          <button className="footer-link" onClick={() => setShowPrivacy(true)}>
            Privacy Policy
          </button>
        </li>
      </ul>

      <Modal 
        show={showTerms} 
        onClose={() => setShowTerms(false)}
        title="Terms of Services"
      >
        <div>
          <h3>1. Acceptance of Terms</h3>
          <p>By accessing and using ChurnIT's services, you agree to be bound by these Terms of Service.</p>

          <h3>2. Use of Services</h3>
          <p>Our services are designed for business use. You agree to use them only for their intended purposes.</p>

          <h3>3. User Accounts</h3>
          <p>You are responsible for maintaining the confidentiality of your account credentials.</p>

          <h3>4. Data Privacy</h3>
          <p>We handle your data in accordance with our Privacy Policy. You retain all rights to your data.</p>

          <h3>5. Service Modifications</h3>
          <p>We reserve the right to modify or discontinue our services with reasonable notice.</p>
        </div>
      </Modal>

      <Modal 
        show={showPrivacy} 
        onClose={() => setShowPrivacy(false)}
        title="Privacy Policy"
      >
        <div>
          <h3>1. Information Collection</h3>
          <p>We collect information you provide directly to us and data about your use of our services.</p>

          <h3>2. Use of Information</h3>
          <p>We use collected information to provide, maintain, and improve our services.</p>

          <h3>3. Data Security</h3>
          <p>We implement appropriate security measures to protect your personal information.</p>

          <h3>4. Data Sharing</h3>
          <p>We do not sell your personal information. We share data only with your consent.</p>

          <h3>5. Your Rights</h3>
          <p>You have the right to access, correct, or delete your personal information.</p>
        </div>
      </Modal>
    </div>
  );
};

export default Footer;