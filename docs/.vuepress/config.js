const path = require("path");
module.exports = {
    title: 'GATE Teamware Documentation',
    description: 'Documentation for GATE Teamware',
    base: "/gate-teamware/",
    themeConfig: {
        // nav: [
        //   { text: 'Home', link: '/' },
        //   { text: 'Guide', link: '/guide/' },
        //   { text: 'External', link: 'https://google.com' }
        // ],
        sidebar: [
            '/',
            {
                title: "User guide",
                children: [
                    "userguide/quickstart",
                    "userguide/overview",
                    "userguide/project_management",
                    "userguide/project_config",
                    "userguide/documents_annotations_management",
                    "userguide/annotators_management",
                ]
            },
            {
                title: "Developer guide",
                children: [
                    'developerguide/',
                    'developerguide/testing',
                    'developerguide/releases',
                    "developerguide/api_docs",
                ]
            },
        ],
    },
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, '../../frontend/src')
            }
        }
    }
}
