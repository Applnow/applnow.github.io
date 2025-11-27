---
layout: page
title: Album
permalink: /album/
---

这里存放一些好看的图片。

<div class="album-grid">
  <!-- 图片将会在这里显示 -->
</div>

<div id="lightbox" class="lightbox">
  <span class="close">&times;</span>
  <img class="lightbox-content" id="lightbox-img">
  <div class="caption" id="lightbox-caption"></div>
  <a class="prev">&#10094;</a>
  <a class="next">&#10095;</a>
</div>

<style>
.album-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.album-item {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.album-item:hover {
  transform: scale(1.05);
}

.album-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.album-caption {
  padding: 0.5rem;
  background: rgba(255,255,255,0.9);
  text-align: center;
  font-size: 0.9rem;
}
.lightbox {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.9);
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.lightbox-content {
  display: block;
  margin: auto;
  max-width: 90%;
  max-height: 80%;
  margin-top: 5%;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.close {
  position: absolute;
  top: 20px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.close:hover {
  color: #bbb;
}

.caption {
  text-align: center;
  color: #ccc;
  padding: 10px 20px;
  position: absolute;
  bottom: 20px;
  width: 100%;
}

.prev, .next {
  cursor: pointer;
  position: absolute;
  top: 50%;
  width: auto;
  padding: 16px;
  margin-top: -50px;
  color: white;
  font-weight: bold;
  font-size: 20px;
  transition: 0.3s;
  user-select: none;
  background-color: rgba(0,0,0,0.5);
  border-radius: 0 3px 3px 0;
}

.next {
  right: 0;
  border-radius: 3px 0 0 3px;
}

.prev:hover, .next:hover {
  background-color: rgba(0,0,0,0.8);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .album-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .lightbox-content {
    max-width: 95%;
    max-height: 70%;
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const albumGrid = document.querySelector('.album-grid');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.querySelector('.close');
  const prevBtn = document.querySelector('.prev');
  const nextBtn = document.querySelector('.next');

  const images = [
    { src: '/public/css/images/background.jpg', caption: 'Koishi Background' },
    { src: '/public/css/images/Yamaxanadu.png', caption: 'Yamaxanadu' },
    { src: '/public/css/images/reimu.jpg', caption: 'Hakurei Jinja' },
    { src: '/public/css/images/壁纸1.png', caption: 'Aya' }
  ];
  
  let currentIndex = 0;
  
  // 渲染图片网格
  function renderAlbum() {
    images.forEach((img, index) => {
      const item = document.createElement('div');
      item.className = 'album-item';
      item.innerHTML = `
        <img src="${img.src}" alt="${img.caption}" loading="lazy">
        <div class="album-caption">${img.caption}</div>
      `;
      
      // 添加点击事件
      item.addEventListener('click', () => openLightbox(index));
      
      albumGrid.appendChild(item);
    });
  }
  
  // 打开灯箱
  function openLightbox(index) {
    currentIndex = index;
    updateLightbox();
    lightbox.style.display = 'block';
    document.body.style.overflow = 'hidden'; // 防止背景滚动
  }
  
  // 关闭灯箱
  function closeLightbox() {
    lightbox.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
  
  // 更新灯箱内容
  function updateLightbox() {
    const currentImage = images[currentIndex];
    lightboxImg.src = currentImage.src;
    lightboxCaption.textContent = currentImage.caption;
  }
  
  // 上一张
  function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateLightbox();
  }
  
  // 下一张
  function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateLightbox();
  }
  
  // 键盘导航
  function handleKeydown(e) {
    if (lightbox.style.display === 'block') {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') prevImage();
      if (e.key === 'ArrowRight') nextImage();
    }
  }
  
  // 事件监听
  closeBtn.addEventListener('click', closeLightbox);
  prevBtn.addEventListener('click', prevImage);
  nextBtn.addEventListener('click', nextImage);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', handleKeydown);
  
  // 初始化相册
  renderAlbum();
});
</script>
