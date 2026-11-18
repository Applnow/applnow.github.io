# 轻文学独立裁判

个人博客，基于 Jekyll 4 + Hyde 主题。

## 仓库结构

```
.
├── _config.yml          # 站点配置
├── Gemfile              # 依赖（插件经 :jekyll_plugins 组加载）
├── Gemfile.lock
├── index.html           # 首页（layout: default，分页 7 篇）
├── 404.html
├── atom.xml             # RSS，手写模板（未使用 jekyll-feed）
├── about.md             # /about/
├── album.html           # /album/ 相册，front matter 中 album: true 触发 assets/album.js
├── friendlink.md        # /friendlink/
├── _includes/
│   ├── head.html        # <head>，引入 assets/css 下三个样式表与 lightbox.css
│   └── sidebar.html     # 侧栏导航
├── _layouts/
│   ├── default.html     # 全站骨架，输出唯一的全局灯箱容器
│   ├── page.html        # 独立页面
│   └── post.html        # 文章
├── _posts/              # 文章（18 篇）
├── assets/              # 全部前端资源
│   ├── css/             # poole.css / syntax.css / hyde.css / lightbox.css
│   ├── images/          # 相册图片（14 张）
│   ├── lightbox.js      # 全局灯箱：文章内图片与相册共用
│   ├── album.js         # 相册图片清单与网格渲染
│   ├── favicon.ico
│   └── apple-touch-icon-144-precomposed.png
└── images/              # 文章内文插图与头像（6 张）
```

## 几个约定

- **图片分两处**：`assets/images/` 放相册图，`images/` 放文章内文插图与头像。
  文章内引用一律写成站点根绝对路径，例如 `![说明](/images/foo.png)`。
  *（此分工为过渡方案，图床/自动托管方案待讨论，见下。）*
- **灯箱只有一套**：容器由 `_layouts/default.html` 输出，样式在 `assets/css/lightbox.css`，
  行为在 `assets/lightbox.js`，它同时收集 `.post img` 与 `.album-grid img`。
  相册页面只需在 `_layouts/default.html` 里通过 `page.album` 开关引入 `assets/album.js`。
- **文章 front matter 的日期**统一为 `date: YYYY-MM-DD HH:MM:SS +0800`。
  注意 Jekyll 不接受 `2025-11-23-21:30:00` 这类用连字符分隔日期与时间的写法，
  那样会静默回退到文件名日期并丢失时间。
- 构建产物 `_site/` 与缓存 `.jekyll-cache/`（含任意嵌套子目录中的同名目录）均已加入 `.gitignore`。

## 本地构建

```bash
bundle install
bundle exec jekyll serve
```

## 待定

- **图片托管**：目前插图的流程是「手动把图放进 `images/`，再在正文里写路径」，较为繁琐。
  计划改为自动化方案（可能使用图床），细节待定；在确定前 `images/` 目录保持现状不动。
