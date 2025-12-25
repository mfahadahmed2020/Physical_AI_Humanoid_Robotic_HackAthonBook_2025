import React from 'react';
import clsx from 'clsx';
import {useDocsSidebar} from '@docusaurus/theme-common/internal';
import {useLocation} from '@docusaurus/router';
import Link from '@docusaurus/Link';
import './TextbookLayout.css';

function TextbookLayout(props) {
  const {children, sidebar, toc, ...layoutProps} = props;
  const {pathname} = useLocation();
  const sidebarData = useDocsSidebar();

  // Check if we're on a textbook page
  const isTextbookPage = pathname.startsWith('/docs');

  return (
    <div className="textbook-container">
      <div className="textbook-layout">
        {isTextbookPage && sidebar && (
          <div className="textbook-sidebar">
            <nav className="textbook-sidebar-nav" aria-label="Docs sidebar">
              <div className="textbook-sidebar-header">
                <h3>Textbook Contents</h3>
              </div>
              
              {sidebarData.items.map((item, index) => (
                <div key={index} className="textbook-sidebar-category">
                  <h4 className="textbook-sidebar-category-title">
                    {item.label}
                  </h4>
                  <ul className="textbook-sidebar-items">
                    {item.items.map((subItem, subIndex) => (
                      <li key={subIndex} className="textbook-sidebar-item">
                        <Link
                          to={subItem.href}
                          className={clsx(
                            'textbook-sidebar-link',
                            subItem.href === pathname && 'textbook-sidebar-link-active'
                          )}
                        >
                          {subItem.label}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </nav>
          </div>
        )}
        
        <main className="textbook-main">
          <div className="textbook-content">
            {children}
          </div>
          
          {toc && (
            <div className="textbook-toc">
              <div className="textbook-toc-header">
                <h3>On this page</h3>
              </div>
              {toc}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default TextbookLayout;