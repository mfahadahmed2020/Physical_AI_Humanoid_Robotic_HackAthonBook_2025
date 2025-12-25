import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Book',
  url: 'https://your-site.com',
  baseUrl: '/',
  favicon: 'img/favicon.ico',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
        htmlLang: 'ur-PK',
      },
    },
  },

  themeConfig: {
    navbar: {
      title: 'Book',
      logo: {
        alt: 'RoboLearn Logo',
        src: 'img/logo.svg',
      },
      style: 'dark',
      items: [
        {
          to: '/docs/intro',
          label: 'Docs',
          position: 'left',
        },
        {
          href: '/login',
          label: 'Log In',
          position: 'right',
          className: 'nav-login-btn',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        }

        ],
    },
    prism: {
      theme: prismThemes.github,
    },
  },
};

export default config;