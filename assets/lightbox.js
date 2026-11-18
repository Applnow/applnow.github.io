// 全局图片灯箱（文章内图片与相册图片共用同一套）
// 约定：_layouts/default.html 输出唯一的 #global-lightbox 容器，样式见 assets/css/lightbox.css，
// 本脚本负责收集可放大的图片、绑定导航，并把文章正文里的图片包成卡片样式。
document.addEventListener('DOMContentLoaded', function () {
    const lightbox = document.getElementById('global-lightbox');
    if (!lightbox) return;

    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const lightboxCaption = lightbox.querySelector('.caption');
    const closeBtn = lightbox.querySelector('.close');
    const prevBtn = lightbox.querySelector('.prev');
    const nextBtn = lightbox.querySelector('.next');

    wrapPostImages();

    // 收集页面上所有可放大的图片：文章正文 + 相册网格
    const images = Array.from(
        document.querySelectorAll('.post img, .album-grid img')
    ).filter(function (img) {
        return !img.closest('#global-lightbox');
    });

    if (images.length === 0) return;

    let currentIndex = 0;

    images.forEach(function (img, index) {
        // 相册条目的图注写在 .album-caption 里，优先取用
        const captionEl = img.closest('.album-item')?.querySelector('.album-caption');
        img.dataset.lightboxCaption =
            (captionEl && captionEl.textContent.trim()) || img.alt || img.title || '';
        img.addEventListener('click', function (e) {
            e.preventDefault();
            open(index);
        });
    });

    function open(index) {
        currentIndex = index;
        update();
        lightbox.style.display = 'block';
        document.body.style.overflow = 'hidden'; // 防止背景滚动
    }

    function close() {
        lightbox.style.display = 'none';
        document.body.style.overflow = '';
    }

    function update() {
        const img = images[currentIndex];
        lightboxImg.src = img.src;
        lightboxImg.alt = img.dataset.lightboxCaption || '';
        lightboxCaption.textContent = img.dataset.lightboxCaption || '';
    }

    function step(delta) {
        currentIndex = (currentIndex + delta + images.length) % images.length;
        update();
    }

    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', function () { step(-1); });
    nextBtn.addEventListener('click', function () { step(1); });
    lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) close();
    });
    document.addEventListener('keydown', function (e) {
        if (lightbox.style.display !== 'block') return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') step(-1);
        if (e.key === 'ArrowRight') step(1);
    });
});

// 把文章正文里的图片包进卡片容器，并显示图注（有图注才显示）
function wrapPostImages() {
    const postContainer = document.querySelector('.post');
    if (!postContainer) return;

    postContainer.querySelectorAll('img').forEach(function (img) {
        if (img.closest('.post-image-card')) return; // 避免重复包裹

        const caption = img.title || img.alt || '';
        const card = document.createElement('div');
        card.className = 'post-image-card';

        img.parentNode.insertBefore(card, img);
        card.appendChild(img);

        if (caption) {
            const captionDiv = document.createElement('div');
            captionDiv.className = 'post-image-caption';
            captionDiv.textContent = caption;
            card.appendChild(captionDiv);
        }
    });
}
