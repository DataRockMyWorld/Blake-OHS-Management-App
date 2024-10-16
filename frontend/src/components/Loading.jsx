import React from 'react';
import '../Loading.css';  // Import your CSS for loading

const Loading = () => {
  return (
    <div className="loading-container">
      <div className="safety-loader">
        <div className="helmet-icon"></div> {/* Helmet Icon */}
      </div>
      <p className="loading-text">Safety first, please wait...</p>
    </div>
  );
};

export default Loading;
