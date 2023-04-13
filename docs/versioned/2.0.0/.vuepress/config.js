const versionData = require("./versions.json")
const path = require("path");
module.exports = context => ({
    title: 'GATE Teamware Documentation',
    description: 'Documentation for GATE Teamware',
    base: versionData.base,
    themeConfig: {
        nav: [
            {text: 'Home', link: '/'},
            {text: 'Annotators', link: '/annotatorguide/'},
            {text: 'Managers & Admins', link: '/manageradminguide/'},
            {text: 'Developer', link: '/developerguide/'}
        ],
        sidebar: {
            '/manageradminguide/': [
                "",
                "project_management",
                "project_config",
                "documents_annotations_management",
                "annotators_management"
            ],
            '/developerguide/': [
                '',
                'testing',
                'releases',
                'documentation',
                "api_docs",

            ],
        },
    },
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, versionData.frontendSource)
            }
        }
    },


})
