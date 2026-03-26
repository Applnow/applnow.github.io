// 全局图片灯箱
document.addEventListener('DOMContentLoaded', function() {
    wrapImagesInPost();
    const lightbox = document.getElementById('global-lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeBtn = lightbox.querySelector('.close');
    const prevBtn = lightbox.querySelector('.prev');
    const nextBtn = lightbox.querySelector('.next');

    let currentImages = [];      // 存储当前页面所有可放大的图片（img 元素）
    let currentIndex = 0;

    // 获取所有文章内容区域的图片（比如 .post 容器内的 img）
    const postImages = document.querySelectorAll('.post img');
    if (postImages.length === 0) return; // 没有图片，不初始化

    // 构建图片数组（存储 src 和 alt）
    postImages.forEach((img, idx) => {
        currentImages.push({
            src: img.src,
            caption: img.alt || (img.title ? img.title : '')
        });
        // 为每个图片添加点击事件
        img.addEventListener('click', (e) => {
            e.preventDefault();
            currentIndex = idx;
            updateLightbox(currentIndex);
            lightbox.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    function wrapImagesInPost() {
    const postContainer = document.querySelector('.post'); // 根据你的文章容器类名调整
    if (!postContainer) return;

    const images = postContainer.querySelectorAll('img:not(.album-grid img)'); // 排除已在相册中的图片
    images.forEach(img => {
        // 避免重复包裹
        if (img.parentElement.classList && img.parentElement.classList.contains('post-image-card')) return;

        // 读取标题（优先用 title，其次 alt）
        const caption = img.title || img.alt || '';

        // 创建卡片容器
        const card = document.createElement('div');
        card.className = 'post-image-card';
        
        // 将原图片移动到卡片中
        img.parentNode.insertBefore(card, img);
        card.appendChild(img);
        
        // 创建标题容器
        if (caption) {
            const captionDiv = document.createElement('div');
            captionDiv.className = 'post-image-caption';
            captionDiv.textContent = caption;
            card.appendChild(captionDiv);
        }
    });
    }

    function updateLightbox(index) {
        const imgData = currentImages[index];
        lightboxImg.src = imgData.src;
        lightboxCaption.textContent = imgData.caption;
    }

    function closeLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
        updateLightbox(currentIndex);
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % currentImages.length;
        updateLightbox(currentIndex);
    }

    // 绑定事件
    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', prevImage);
    nextBtn.addEventListener('click', nextImage);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
        if (lightbox.style.display === 'block') {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') prevImage();
            if (e.key === 'ArrowRight') nextImage();
        }
    });
});
