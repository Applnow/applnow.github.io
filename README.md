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
├── images/              # 文章内文插图与头像（6 张）
├── _img/                # 图片工作区（Jekyll 不下划线目录，不会进 _site）
│   ├── originals/       # 按原始相对路径保存的处理前原图（可随时重新压缩）
│   └── manifest.json    # 处理记录：旧名→新名、内容哈希、体积变化
└── tools/               # 图片处理脚本（见下）
```

## 几个约定

- **图片分两处**：`assets/images/` 放相册图，`images/` 放文章内文插图与头像。
  文章内引用一律写成站点根绝对路径，例如 `![登上 Kaggle Leaderboard](/images/kaggle-leaderboard-80fafb0c.webp)`。
- **图片命名统一由工具生成**，不要手工起名。规则是：

  ```
  <语义名>-<内容哈希前 8 位>.webp
  ```

  语义名由原文件名归一而来（小写、空格转连字符、中文转写），
  哈希取自**处理后的文件内容**。这样同一张图重复处理得到同一个名字，
  不同内容的图永不撞名——不需要查重，也不需要人工避让。
  处理前的原图都留了一份在 `_img/originals/`，随时可以重新压缩。
- **灯箱只有一套**：容器由 `_layouts/default.html` 输出，样式在 `assets/css/lightbox.css`，
  行为在 `assets/lightbox.js`，它同时收集 `.post img` 与 `.album-grid img`。
  相册页面只需在 `_layouts/default.html` 里通过 `page.album` 开关引入 `assets/album.js`。
- **灯箱下方的图注来自 `alt`**：`assets/lightbox.js` 的取词优先级是
  `.album-caption` 文本 > `img.alt` > `img.title`。所以正文写 `![说明](url)` 时
  **不要省略方括号里的说明**——它就是灯箱里显示的那行字，也是文章内图片卡片下方的图注。
- **文章 front matter 的日期**统一为 `date: YYYY-MM-DD HH:MM:SS +0800`。
  注意 Jekyll 不接受 `2025-11-23-21:30:00` 这类用连字符分隔日期与时间的写法，
  那样会静默回退到文件名日期并丢失时间。
- 构建产物 `_site/` 与缓存 `.jekyll-cache/`（含任意嵌套子目录中的同名目录）均已加入 `.gitignore`。

## 图片处理

`tools/` 下是图片处理脚本。首次使用先建虚拟环境（只需一次）：

```bash
python3 -m venv tools/.venv
tools/.venv/bin/pip install Pillow
```

**把仓库里已有的图片压成 WebP 并统一命名**：

```bash
tools/.venv/bin/python tools/normalize-images.py            # 预报，不改动任何文件
tools/.venv/bin/python tools/normalize-images.py --write    # 真正执行
```

默认只做预报。加 `--write` 才会写盘，且写入前会把每个原文件备份到
`_img/originals/` 下的原始相对路径，所以这一步是可逆的。
脚本是幂等的：已经是规范名字的图不会被动。

注意：文件名一变，引用它们的地方就要同步改写（`grep -rn "旧文件名" .` 可以找出全部引用点）。

## 本地构建

```bash
bundle install
bundle exec jekyll serve
```

## 图片托管（Cloudflare R2）

图片正文里照常写本地路径，跑一条命令上传到 R2，脚本把链接回填成外链：

```bash
tools/.venv/bin/python tools/upload-images.py                    # 预报：只看会传哪些
tools/.venv/bin/python tools/upload-images.py --apply            # 上传并回填
```

默认只预报。两条硬约束是刻意设计的：

- **不动方括号里的说明文字**。`![说明](url)` 的说明会进 `img.alt`，
  而灯箱下方的图注正是从 alt 取的——脚本只替换 URL 部分。
- **跑第二遍不会重复上传**。账本记在 `_img/uploaded.json`，键是文件内容的哈希，
  所以改名、换目录、同一张图被多篇文章引用，都不会二次上传。

### 首次配置

1. Cloudflare 控制台建一个 R2 存储桶，记下账户 ID（endpoint 是
   `https://<账户ID>.r2.cloudflarestorage.com`）。
2. 建 API 令牌，权限只需 **Object Read & Write**，范围限定到那个桶。
3. 绑一个自定义域名指向该桶，作为 `public_base`。**不要用 `r2.dev` 那个域名**——
   那是受限的测试域名，有速率限制，不适合生产。
4. 复制 `_img/r2.json.example` 为 `_img/r2.json` 并填好字段：

   ```json
   {
     "endpoint": "https://<账户ID>.r2.cloudflarestorage.com",
     "bucket": "你的桶名",
     "access_key_id": "...",
     "secret_access_key": "...",
     "public_base": "https://你的自定义域名",
     "prefix": "blog"
   }
   ```

`_img/r2.json` 已在 `.gitignore` 里，密钥不会进版本库。

### 日常流程

1. 把图片放进仓库（`images/` 或 `assets/images/`），正文写 `![说明](/images/xxx.png)`。
2. 跑 `--apply`。脚本会压缩、按统一规则改名、上传、回填链接。
3. 提交正文改动即可，图片不必再提交。

**注意**：本机没有 ruby/Jekyll，`tools/` 里的脚本只能用 `tools/.venv/bin/python` 跑，
无法在这里验证 Jekyll 构建结果。改动后请在本地跑一次 `bundle exec jekyll serve`。
