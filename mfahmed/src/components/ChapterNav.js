import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import './ChapterNav.css';

function ChapterNav({previous, next}) {
  return (
    <div className="chapter-navigation">
      {previous && (
        <Link to={previous.path} className="chapter-nav-link chapter-nav-previous">
          ← {previous.title}
        </Link>
      )}
      
      {next && (
        <Link to={next.path} className="chapter-nav-link chapter-nav-next">
          {next.title} →
        </Link>
      )}
    </div>
  );
}

export default ChapterNav;