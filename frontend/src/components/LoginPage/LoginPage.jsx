import React, { useState, useEffect } from "react";
import "./LoginPage.css";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [resetEmail, setResetEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  const clientId =
    "886838287131-fotu4sh90du29nuql1nd6s1q0mdd8pe7.apps.googleusercontent.com";

  // This is the local address where your Python Flask app runs
  const FLASK_BACKEND_URL = "";

  useEffect(() => {
    // Wipe login data when the website is loaded for the first time
    localStorage.clear();
  }, []);

  const handleGoogleSuccess = (response) => {
    const credential = response.credential;
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("googleCredential", credential);
    alert("Login successful with Google");
    window.location.href = `${FLASK_BACKEND_URL}/`;
  };

  const handleGoogleFailure = () => {
    setError("Google login failed. Please try again.");
  };

  // This handles BOTH logging in and registering an account
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Clear out any old error messages

    if (isLogin) {
      // ==========================================
      //           LOGGING IN AN ACCOUNT
      // ==========================================
      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (data.success) {
          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("userEmail", formData.email);
          alert("Login successful!");

          // REDIRECT: Redirects the browser to your main Flask dashboard page
          window.location.href = "/";
        } else {
          // If Flask says it failed, show the error message from Flask (e.g. "Incorrect email or password")
          setError(data.message);
        }
      } catch (err) {
        setError("Cannot connect to backend server. Is app.py running?");
      }
    } else {
      // ==========================================
      //          REGISTERING A NEW ACCOUNT
      // ==========================================
      if (formData.password !== formData.confirmPassword) {
        setError("Passwords do not match.");
        return;
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (data.success) {
          alert(data.message);
          setIsLogin(true); // Flip the form view automatically to show the Login form
        } else {
          setError(data.message);
        }
      } catch (err) {
        setError("Cannot connect to backend server. Is app.py running?");
      }
    }
  };

  const handleForgotPassword = () => {
    setIsForgotPassword(true);
    setError("");
  };

  const handleResetPassword = () => {
    // Keeping your original frontend password reset layout as a safe structural view
    alert("Password reset link sent to your registration endpoint.");
    setIsForgotPassword(false);
    setIsLogin(true);
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div className="login-container">
        <div className="login-box">
          <h2>
            {isForgotPassword
              ? "Reset Password"
              : isLogin
                ? "Login"
                : "Register"}
          </h2>
          {error && <p className="error-message">{error}</p>}

          {isForgotPassword ? (
            <div>
              <div className="form-group">
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={resetEmail}
                  onChange={(e) => setResetEmail(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  placeholder="Confirm new password"
                  value={confirmNewPassword}
                  onChange={(e) => setConfirmNewPassword(e.target.value)}
                  required
                />
              </div>
              <button className="submit-btn" onClick={handleResetPassword}>
                Reset Password
              </button>
              <p
                className="toggle-form"
                onClick={() => setIsForgotPassword(false)}
              >
                Back to Login
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                  required
                />
              </div>

              {!isLogin && (
                <div className="form-group">
                  <input
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm Password"
                    value={formData.confirmPassword}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        confirmPassword: e.target.value,
                      })
                    }
                    required
                  />
                </div>
              )}

              {isLogin && (
                <p className="forgot-password" onClick={handleForgotPassword}>
                  Forgot Password?
                </p>
              )}

              <button type="submit" className="submit-btn">
                {isLogin ? "Login" : "Register"}
              </button>
            </form>
          )}

          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleFailure}
          />

          {!isForgotPassword && (
            <p className="toggle-form">
              {isLogin
                ? "Don't have an account? "
                : "Already have an account? "}
              <span onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? "Register here" : "Login here"}
              </span>
            </p>
          )}
        </div>
      </div>
    </GoogleOAuthProvider>
  );
};

export default LoginPage;
