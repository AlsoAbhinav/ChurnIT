import React, { useState, useEffect } from "react";

const AuthPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [forgotPassword, setForgotPassword] = useState(false);
  const [changePassword, setChangePassword] = useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem("authenticatedUser");
    if (storedUser) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    const storedUsers = JSON.parse(localStorage.getItem("users")) || {};
    if (storedUsers[username] && storedUsers[username] === password) {
      localStorage.setItem("authenticatedUser", username);
      setIsAuthenticated(true);
      setError("");
    } else {
      setError("Invalid credentials! Please register if you don't have an account.");
    }
  };

  const handleRegister = () => {
    let storedUsers = JSON.parse(localStorage.getItem("users")) || {};
    if (storedUsers[username]) {
      setError("User already exists! Try logging in.");
    } else {
      storedUsers[username] = password;
      localStorage.setItem("users", JSON.stringify(storedUsers));
      localStorage.setItem("authenticatedUser", username);
      setIsAuthenticated(true);
      setError("");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("authenticatedUser");
    setIsAuthenticated(false);
  };

  const handleForgotPassword = () => {
    let storedUsers = JSON.parse(localStorage.getItem("users")) || {};
    if (!storedUsers[username]) {
      setError("User not found! Please register first.");
      return;
    }
    setForgotPassword(true);
    setError("");
  };

  const handleResetPassword = () => {
    let storedUsers = JSON.parse(localStorage.getItem("users")) || {};
    if (!storedUsers[username]) {
      setError("User not found! Please register first.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match!");
      return;
    }
    storedUsers[username] = newPassword;
    localStorage.setItem("users", JSON.stringify(storedUsers));
    setError("");
    setForgotPassword(false);
    alert("Password has been reset. Please log in.");
  };

  const handleChangePassword = () => {
    let storedUsers = JSON.parse(localStorage.getItem("users")) || {};
    const currentUser = localStorage.getItem("authenticatedUser");
    if (storedUsers[currentUser] !== password) {
      setError("Current password is incorrect!");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("New passwords do not match!");
      return;
    }
    storedUsers[currentUser] = newPassword;
    localStorage.setItem("users", JSON.stringify(storedUsers));
    setError("");
    setChangePassword(false);
    alert("Password changed successfully.");
  };

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <h2>Welcome, {localStorage.getItem("authenticatedUser")}!</h2>
          <button onClick={() => setChangePassword(true)}>Change Password</button>
          <button onClick={handleLogout}>Logout</button>

          {changePassword && (
            <div>
              <h3>Change Password</h3>
              <input type="password" placeholder="Current Password" onChange={(e) => setPassword(e.target.value)} />
              <input type="password" placeholder="New Password" onChange={(e) => setNewPassword(e.target.value)} />
              <input type="password" placeholder="Confirm New Password" onChange={(e) => setConfirmPassword(e.target.value)} />
              <button onClick={handleChangePassword}>Update Password</button>
              <button onClick={() => setChangePassword(false)}>Cancel</button>
              {error && <p style={{ color: "red" }}>{error}</p>}
            </div>
          )}
        </div>
      ) : forgotPassword ? (
        <div>
          <h2>Reset Password</h2>
          <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
          <input type="password" placeholder="New Password" onChange={(e) => setNewPassword(e.target.value)} />
          <input type="password" placeholder="Confirm New Password" onChange={(e) => setConfirmPassword(e.target.value)} />
          <button onClick={handleResetPassword}>Reset Password</button>
          <button onClick={() => setForgotPassword(false)}>Cancel</button>
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      ) : (
        <div>
          <h2>Login/Register</h2>
          <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleRegister}>Register</button>
          <button onClick={handleForgotPassword}>Forgot Password?</button>
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      )}
    </div>
  );
};

export default AuthPage;
