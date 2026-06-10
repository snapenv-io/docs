import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SnapEnv',
  description: 'Secure environment variables for dev teams',
  lang: 'en-US',
  cleanUrls: true,

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#6366f1' }],
  ],

  themeConfig: {
    logo: '/favicon.svg',
    siteTitle: 'SnapEnv Docs',

    nav: [
      { text: 'Guide',        link: '/guide/introduction' },
      { text: 'CLI',          link: '/guide/cli' },
      { text: 'API',          link: '/api/overview' },
      { text: 'Integrations', link: '/integrations/overview' },
      {
        text: 'snapenv.io',
        items: [
          { text: 'Dashboard', link: 'https://dash.snapenv.io' },
          { text: 'Website',   link: 'https://snapenv.io' },
        ],
      },
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Getting started',
          items: [
            { text: 'Introduction',    link: '/guide/introduction' },
            { text: 'Quick start',     link: '/guide/quick-start' },
            { text: 'Authentication',  link: '/guide/authentication' },
          ],
        },
        {
          text: 'CLI',
          items: [
            { text: 'Installation',    link: '/guide/cli' },
            { text: 'pull',            link: '/guide/cli-pull' },
            { text: 'push',            link: '/guide/cli-push' },
            { text: 'diff',            link: '/guide/cli-diff' },
            { text: 'projects',        link: '/guide/cli-projects' },
            { text: 'upgrade',         link: '/guide/cli-upgrade' },
          ],
        },
        {
          text: 'Dashboard',
          items: [
            { text: 'Variables',       link: '/guide/variables' },
            { text: 'Environments',    link: '/guide/environments' },
            { text: 'Team & access',   link: '/guide/team' },
            { text: 'Access tokens',   link: '/guide/tokens' },
            { text: 'Variable expiry', link: '/guide/expiry' },
            { text: 'Webhooks',        link: '/guide/webhooks' },
            { text: 'Audit log',       link: '/guide/audit' },
          ],
        },
        {
          text: 'Security',
          items: [
            { text: 'Encryption',      link: '/guide/encryption' },
            { text: '2FA',             link: '/guide/2fa' },
            { text: 'Permissions',     link: '/guide/permissions' },
          ],
        },
      ],
      '/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'Overview',        link: '/api/overview' },
            { text: 'Authentication',  link: '/api/authentication' },
            { text: 'Projects',        link: '/api/projects' },
            { text: 'Variables',       link: '/api/variables' },
            { text: 'Tokens',          link: '/api/tokens' },
            { text: 'Workspace',       link: '/api/workspace' },
            { text: 'Webhooks',        link: '/api/webhooks' },
            { text: 'Audit',           link: '/api/audit' },
          ],
        },
      ],
      '/integrations/': [
        {
          text: 'Integrations',
          items: [
            { text: 'Overview',             link: '/integrations/overview' },
            { text: 'Kubernetes Operator',  link: '/integrations/kubernetes' },
            { text: 'GitHub Actions',       link: '/integrations/github-actions' },
            { text: 'Docker / Compose',     link: '/integrations/docker' },
            { text: 'Init containers',      link: '/integrations/init-container' },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/snapenv-io' },
    ],

    search: { provider: 'local' },

    footer: {
      message: 'Built with SnapEnv',
      copyright: '© 2026 SnapEnv',
    },

    editLink: {
      pattern: 'https://github.com/snapenv-io/docs/edit/main/:path',
      text: 'Edit this page on GitHub',
    },
  },
})
