import React from 'react';
import clsx from 'clsx';
import './ProgressIndicator.css';

function ProgressIndicator({current, total, chapterTitle}) {
  const percentage = Math.round((current / total) * 100);
  
  return (
    <div className="progress-container">
      <div className="progress-header">
        <span className="progress-text">
          Chapter {current} of {total}: {chapterTitle}
        </span>
        <span className="progress-percentage">{percentage}%</span>
      </div>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      <div className="progress-details">
        <span className="progress-status">
          {current === 1 ? 'Just getting started!' : 
           current === total ? 'Congratulations! You\'ve completed this section.' : 
           `Keep going! ${total - current} chapters remaining.`}
        </span>
      </div>
    </div>
  );
}

export default ProgressIndicator;