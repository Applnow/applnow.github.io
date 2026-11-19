---
layout: page
title: About Me
permalink: /about/
---
<div class="profile-avatar">
  <!-- 头像直接取 GitHub 账号的公开头像：账号那边换了头像，这里自动跟着换，不必再手工上传。
       github.com/Applnow.png 会 302 到 avatars.githubusercontent.com 并带上最新版本号；
       size=460 是 GitHub 允许的最大边长，而显示尺寸只有 180px（见下方 .profile-avatar），
       给高分屏留足余量。万一该域名加载不到（部分网络下会不通），回退到原先托管的静态图。 -->
  <img src="https://github.com/Applnow.png?size=460"
       onerror="this.onerror=null;this.src='https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/your-avatar-87cb8efa.webp'"
       alt="我的头像">
</div>
<div class="about-content">
  <h1><span class="highlight">苹雪_の避难所</span></h1>
<div class="intro-section">
    <p class="lead">Call me Ishamel.</p>
<p>浙江省苍南县人氏。北外温附遗民。暖州中学难民。
现就读于上海市自由而无用大学。</p>
<p>不知名东方project爱好者，Yu-Gi-Oh前玩家，动漫低手，国内宅文化原教旨主义者，部分时间是轻文学读者。</p>
<p>术力口、月计、独立游戏、型月、三国杀、电子竞技、网哲见证、抽象文化、网络迷因、格斗游戏、钓鱼反串都略懂一点。</p>

<p>对普通人类没有兴趣。如果你们当中有外星人、未来人、超能力者的话，就尽管来找我吧。以上。</p>
</div>

<section class="license-section">
  <h2>内容许可</h2>
  <p>除特别注明（或另有声明）外，本站所有原创文字内容均采用
  <a href="https://creativecommons.org/licenses/by/4.0/deed.zh" target="_blank" rel="license noopener">知识共享「署名 4.0 国际」（CC BY 4.0）</a>
  许可协议授权。</p>
  <ul>
    <li>你可以自由地复制、转载、改编本站内容，包括用于商业目的。</li>
  </ul>
  <p class="license-note">文中引用、翻译或转载他人的作品，著作权归原作者所有。
  评论区内容由评论者本人创作，其权利归评论者所有。</p>
    <p class="license-note">本站的图片资源来源于互联网，如果侵犯了你的版权，请联系<a href="malito:applnow@126.com">applnow@126.com</a>通知我删除。</p>

  <h2>本站用到的开源项目</h2>
  <p>本站是一个静态站点，由下列开源项目驱动，谨向作者与社区致谢：</p>
  <div class="license-table-wrap">
    <table class="license-table">
      <thead>
        <tr><th>项目</th><th>用途</th><th>许可协议</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><a href="https://giscus.app/zh-CN" target="_blank" rel="noopener">giscus</a></td>
          <td>评论系统</td>
          <td>MIT</td>
        </tr>
        <tr>
          <td><a href="https://jekyllrb.com/" target="_blank" rel="noopener">Jekyll</a></td>
          <td>构建静态页面</td>
          <td>MIT</td>
        </tr>
        <tr>
          <td><a href="https://kramdown.gettalong.org/" target="_blank" rel="noopener">kramdown</a> /
              <a href="https://github.com/rouge-ruby/rouge" target="_blank" rel="noopener">Rouge</a></td>
          <td>Markdown 解析</td>
          <td>MIT</td>
        </tr>
        <tr>
          <td><a href="https://github.com/poole/poole" target="_blank" rel="noopener">Poole</a> /
              <a href="https://github.com/poole/hyde" target="_blank" rel="noopener">Hyde</a></td>
          <td>页面排版与主题基础</td>
          <td>MIT</td>
        </tr>
        <tr>
          <td><a href="https://github.com/jekyll/jekyll-seo-tag" target="_blank" rel="noopener">jekyll-seo-tag</a> /
              <a href="https://github.com/jekyll/jekyll-sitemap" target="_blank" rel="noopener">jekyll-sitemap</a></td>
          <td>SEO 元数据</td>
          <td>MIT</td>
        </tr>
        <tr>
          <td><a href="https://github.com/notofonts/noto-cjk" target="_blank" rel="noopener">Noto Serif SC</a></td>
          <td>正文字体</td>
          <td>SIL OFL 1.1</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>关于评论区（giscus）</h3>
  <p>评论功能由开源项目 giscus 提供。它借助 GitHub Discussions 实现评论，
  没有数据库，也没有本站自己的后端：评论与 emoji 反应都以 discussion 的形式
  保存在本站的 GitHub 仓库里。</p>
  <ul>
    <li>发言需要 GitHub 账号，并授权 <a href="https://github.com/apps/giscus" target="_blank" rel="noopener">giscus app</a> 代你发布内容。</li>
    <li>本站不额外收集、存储访客数据；但评论一经发布即在 GitHub 上公开，
        并受 GitHub 服务条款与隐私政策约束。</li>
  </ul>
</section>
<style>
/* 右上角头像样式 */
.profile-avatar {
  position: fixed;
  top: 2rem;
  right: 2rem;
  width: 180px;
  height: 180px;
  z-index: 100;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  background: white;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.profile-avatar img:hover {
  transform: scale(1.05);
}
.about-content,
.about-content p,
.about-content li,
.intro-section,
.detail-card {
    font-family: 'Noto Serif SC', serif, "SimSun", "宋体";
    /* 保持原有中文字体作为后备 */
}
/* 主要内容区域 */
.about-content {
  max-width: 80rem;
  margin-right: 50px; /* 为头像留出空间 */
  position: relative;
  z-index: 1;
}

.about-content h1 {
  font-family: "Abril Fatface", serif;
  font-size: 2.8rem;
  margin-bottom: 1.5rem;
  color: #333;
  line-height: 1.2;
}

.highlight {
  color: #268bd2;
  font-weight: bold;
}

.intro-section {
  margin-bottom: 3rem;
  line-height: 1.7;
  font-size: 1.1rem;
}

.intro-section .lead {
  font-size: 1.3rem;
  font-weight: bold;
  color: #444;
  border-left: 4px solid #268bd2;
  padding-left: 1rem;
  margin-bottom: 1.5rem;
}

/* 详情网格布局 */
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.detail-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-top: 4px solid #268bd2;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.detail-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.detail-card h2 {
  font-size: 1.4rem;
  margin-top: 0;
  margin-bottom: 1.2rem;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-card ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.detail-card li {
  margin-bottom: 1.2rem;
  padding-bottom: 1.2rem;
  border-bottom: 1px dashed #eee;
}

.detail-card li:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.detail-card strong {
  color: #222;
  display: block;
  margin-bottom: 0.3rem;
}

.meta {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
  display: block;
  margin: 0.3rem 0;
}

.contact-list li {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  border-bottom: none;
  padding-bottom: 0.7rem;
  margin-bottom: 0.7rem;
}

.contact-list a {
  text-decoration: none;
  color: #268bd2;
  transition: color 0.2s;
}

.contact-list a:hover {
  color: #1c7199;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-avatar {
    position: relative;
    top: auto;
    right: auto;
    width: 150px;
    height: 150px;
    margin: 0 auto 2rem;
    display: block;
  }

  .about-content {
    margin-right: 0;
    max-width: 100%;
  }

  .about-content h1 {
    font-size: 2.2rem;
    text-align: center;
  }

  .details-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .intro-section .lead {
    font-size: 1.2rem;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .profile-avatar {
    border-color: rgba(50, 50, 50, 0.9);
  }

  .detail-card {
    background: rgba(40, 40, 40, 0.9);
    color: #ddd;
  }

  .detail-card h2,
  .detail-card strong,
  .about-content h1 {
    color: #eee;
  }

  .meta {
    color: #aaa;
  }
}
.layout-page .content { /* .layout-page 可以更精确地定位到使用page布局的页面 */
    max-width: 80rem !important; /* 使用 !important 确保覆盖原有样式 */
}

/* 内容许可与开源说明（位于 About Me 正文下方） */
.license-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px dashed #ddd;
  line-height: 1.7;
}

.license-section h2 {
  font-family: "Abril Fatface", "Noto Serif SC", serif;
  font-size: 1.6rem;
  color: #333;
  margin: 2.5rem 0 1rem;
}

.license-section h2:first-child {
  margin-top: 0;
}

.license-section h3 {
  font-size: 1.2rem;
  color: #333;
  margin: 2rem 0 0.8rem;
}

.license-section ul {
  padding-left: 1.4rem;
  margin: 0.6rem 0 1rem;
}

.license-section li {
  margin-bottom: 0.5rem;
}

.license-section a {
  color: #268bd2;
  text-decoration: none;
}

.license-section a:hover {
  color: #1c7199;
  text-decoration: underline;
}

.license-note {
  font-size: 0.9rem;
  color: #777;
}

.license-table-wrap {
  overflow-x: auto;
  margin: 1rem 0 1.5rem;
}

.license-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.license-table th,
.license-table td {
  text-align: left;
  vertical-align: top;
  padding: 0.6rem 0.8rem;
  border-bottom: 1px solid #eee;
}

.license-table th {
  color: #555;
  font-weight: 600;
  border-bottom: 2px solid #268bd2;
  white-space: nowrap;
}

.license-table td:last-child {
  white-space: nowrap;
}

.license-table code {
  font-size: 0.85em;
  padding: 0.1em 0.3em;
  border-radius: 3px;
  background: rgba(38, 139, 210, 0.08);
}

@media (max-width: 768px) {
  .license-section h2 {
    font-size: 1.4rem;
  }

  .license-table th,
  .license-table td {
    padding: 0.5rem 0.6rem;
    font-size: 0.9rem;
  }
}

@media (prefers-color-scheme: dark) {
  .license-section {
    border-top-color: #444;
  }

  .license-section h2,
  .license-section h3 {
    color: #eee;
  }

  .license-note {
    color: #aaa;
  }

  .license-table th {
    color: #ccc;
  }

  .license-table th,
  .license-table td {
    border-bottom-color: #3a3a3a;
  }

  .license-table code {
    background: rgba(38, 139, 210, 0.2);
  }
}
</style>
