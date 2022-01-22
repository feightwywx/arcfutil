module.exports = {
  locales: {
    '/': {
      lang: 'zh-CN',
      title: 'arcfutil',
      description: '为处理Arcaea相关文件（谱面，songlist，etc.）设计的Python模块。',
    }
  },
  themeConfig: {
    sidebar: [
      {
        title: '快速上手',   // 必要的
        path: '/guide/',      // 可选的, 标题的跳转链接，应为绝对路径且必须存在
        collapsable: false, // 可选的, 默认值是 true,
        sidebarDepth: 2,    // 可选的, 默认值是 1
        children: [
          '/guide/', '/guide/install', '/guide/package-aff', '/guide/easing','/guide/cli-tools', '/guide/cv'
        ]
      },
      {
        title: 'API',   // 必要的
        path: '/api/',
        sidebarDepth: 1,    // 可选的, 默认值是 1
        children: [
          '/api/aff', '/api/aff-easing', '/api/aff-generator', '/api/aff-note', '/api/aff-note-validstrings', '/api/cv','/api/exception',
        ]
      }
    ],
    nav: [
      { text: '首页', link: '/' },
      { text: '快速上手', link: '/guide/' },
      { text: 'API', link: '/api/' },
      {
        text: 'v0.8.1', items: [
          { text: 'v0.8.1', link: '/' }
        ]
      },
      { text: 'AFF工具箱', link: 'https://aff.arcaea.icu/' }
    ],
    // 假定是 GitHub. 同时也可以是一个完整的 GitLab URL
    repo: 'feightwywx/arcfutil',
    // 假如文档不是放在仓库的根目录下：
    docsDir: 'docs',
    // 默认是 false, 设置为 true 来启用
    editLinks: true,
    // 默认为 "Edit this page"
    editLinkText: '帮助我们改善此页面！'
  },
}
