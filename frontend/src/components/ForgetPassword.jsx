import React, { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import { toast } from "react-toastify";
import Loading from "./Loading";  // Import the Loading component

const ForgetPassword = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);  // Manage loading state

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (email) {
      setIsLoading(true);  // Start loading when the request starts
      try {
        const res = await axiosInstance.post('v1/password-reset/', { "email": email });
        if (res.status === 200) {
          toast.success("Password reset link sent successfully to your email");
        }
      } catch (error) {
        toast.error("Something went wrong. Please try again.");
      } finally {
        setIsLoading(false);  // Stop loading once the request completes
      }
    }
    setEmail('');
  };

  // Show the loading component if the request is in progress
  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <h2>Enter your email to reset your password</h2>
      <div className="wrapper">
        <form action="" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="">Email Address:</label>
            <input
              type="email"
              className="email-form"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="vbtn">Send</button>
        </form>
      </div>
    </div>
  );
};

export default ForgetPassword;

