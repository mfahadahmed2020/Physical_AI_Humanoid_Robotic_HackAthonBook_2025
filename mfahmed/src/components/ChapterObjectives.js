import React from 'react';
import clsx from 'clsx';
import './ChapterObjectives.css';

function ChapterObjectives({objectives}) {
  return (
    <div className="learning-objectives">
      <h3>Learning Objectives</h3>
      <ul>
        {objectives.map((objective, index) => (
          <li key={index}>{objective}</li>
        ))}
      </ul>
    </div>
  );
}

export default ChapterObjectives;