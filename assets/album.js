// 相册页的图片清单与网格渲染。
// 仅负责「有哪些图片、怎么排布」；点击放大由 assets/lightbox.js 的全局灯箱统一处理，
// 因此这里不再包含任何灯箱逻辑。
document.addEventListener('DOMContentLoaded', function () {
    const albumGrid = document.querySelector('.album-grid');
    if (!albumGrid) return;

    const images = [
        { src: '/assets/images/background.jpg', caption: 'Koishi Background' },
        { src: '/assets/images/Yamaxanadu.png', caption: 'Yamaxanadu' },
        { src: '/assets/images/reimu.jpg', caption: 'Hakurei Jinja' },
        { src: '/assets/images/壁纸1.png', caption: 'Aya' },
        { src: '/assets/images/draculas.jpg', caption: 'Draculas' },
        { src: '/assets/images/Knowledge.jpg', caption: 'Knowledge' },
        { src: '/assets/images/Library.jpg', caption: 'ヴワル魔法図書館' },
        { src: '/assets/images/Mutsumi.jpg', caption: 'Mutsumi' },
        { src: '/assets/images/Patchouli Knowledge.jpg', caption: 'Patchouli Knowledge' },
        { src: '/assets/images/Personal Preference.jpg', caption: 'Personal Preference' },
        { src: '/assets/images/Sakura.jpg', caption: 'Sakura' },
        { src: '/assets/images/Tianyi.jpg', caption: 'Tianyi Luo' },
        { src: '/assets/images/Doremi.jpg', caption: 'Doremi' }
    ];

    images.forEach(function (img) {
        const item = document.createElement('div');
        item.className = 'album-item';
        item.innerHTML = `
      <img src="${img.src}" alt="${img.caption}" loading="lazy">
      <div class="album-caption">${img.caption}</div>
    `;
        albumGrid.appendChild(item);
    });
});
