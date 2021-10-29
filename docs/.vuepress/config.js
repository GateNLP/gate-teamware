module.exports = {
  title: 'Gate Annotation Service Documentation',
  description: 'Documentation for gate annotation service',
  base: "/gate-annotation-service/",
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
            "userguide/projectconfig",
            "userguide/api_docs"
        ]
      },
        ],
  }
}
