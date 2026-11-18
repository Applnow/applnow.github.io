source "https://rubygems.org"

gem "jekyll", "~> 4.3.1"

# Jekyll 插件（须放在 :jekyll_plugins 组内才会被自动加载）
# 说明：本站 RSS 由手写的 atom.xml 提供，仍未使用 jekyll-feed 的 feed_meta。
#       jekyll-seo-tag / jekyll-sitemap 已启用，二者都在 GitHub Pages 插件白名单内
#       （github-pages gem 222 的依赖里钉死为 seo-tag 2.9.1、sitemap 1.4.0），
#       所以线上构建与本地都能直接加载，无需 CI。
#       seo 标签在 _includes/head.html 中输出，sitemap 由插件自动生成 /sitemap.xml。
group :jekyll_plugins do
  gem "jekyll-paginate"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  # gem "jekyll-feed"
end
