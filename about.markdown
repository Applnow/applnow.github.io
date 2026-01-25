---
layout: page
title: About Me
permalink: /about/
---
<div class="profile-avatar">
  <img src="/images/your-avatar.jpg" alt="我的头像">
</div>
<div class="about-content">
  <h1><span class="highlight">那年Apple雪の避难所</span></h1>
<div class="intro-section">
    <p class="lead">Call me Ishamel.</p>
<p>浙江省苍南县人氏。北外温附遗民。暖州中学难民。
现就读于上海市自由而无用大学。</p>
<p>不知名东方project爱好者，Yu-Gi-Oh前玩家，动漫低手，国内宅文化原教旨主义者，部分时间是轻文学读者。</p>
<p>术力口、月计、文野、独立游戏、三国杀、网哲见证、格斗游戏、型月都略懂一点。</p>
<p>最大的爱好或许是观察离群的人。此类人倒是有很多名字，“神人”“嘉豪”等称谓皆有人叫。本人倒是懒得先下定论，只是先接触着，实在有趣。</p>
<p>对普通人类没有兴趣。如果你们当中有外星人、未来人、超能力者的话，就尽管来找我吧。以上。</p>
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
</style>
