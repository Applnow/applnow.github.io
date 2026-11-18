// 相册页的图片清单与网格渲染。
// 仅负责「有哪些图片、怎么排布」；点击放大由 assets/lightbox.js 的全局灯箱统一处理，
// 因此这里不再包含任何灯箱逻辑。
document.addEventListener('DOMContentLoaded', function () {
    const albumGrid = document.querySelector('.album-grid');
    if (!albumGrid) return;

    const images = [
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/background-16926d0e.webp', caption: 'Koishi Background' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/yamaxanadu-1ffd80c6.webp', caption: 'Yamaxanadu' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/reimu-af1a580d.webp', caption: 'Hakurei Jinja' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/aya-ac435c3c.webp', caption: 'Aya' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/draculas-3016031e.webp', caption: 'Draculas' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/knowledge-tome-98d0ed7d.webp', caption: 'Knowledge' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/library-6060ee9c.webp', caption: 'ヴワル魔法図書館' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/mutsumi-f6efb346.webp', caption: 'Mutsumi' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/patchouli-knowledge-4608d786.webp', caption: 'Patchouli Knowledge' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/personal-preference-71e44ba9.webp', caption: 'Personal Preference' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/sakura-f817bd27.webp', caption: 'Sakura' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/tianyi-06203f50.webp', caption: 'Tianyi Luo' },
        { src: 'https://pub-1808029ad8d1476e96cf6889e47c0bf2.r2.dev/blog/doremi-2bbe6dc2.webp', caption: 'Doremi' }
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
