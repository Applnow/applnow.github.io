/**
 * R2 图片的公开读取入口（Cloudflare Worker 模板）
 *
 * 为什么需要它：R2 的自定义域名要求你拥有一个已托管到 Cloudflare 的域名，
 * 而 `r2.dev` 是受限的测试域名（限速，官方明确说不适合生产）。
 * workers.dev 是免费子域名、不需要买域名，所以用它当图片入口。
 *
 * 部署（两种任选其一）：
 *
 *   1. 控制台：Workers & Pages → 创建 Worker → 编辑代码，粘贴本文件内容。
 *      然后在 Settings → Bindings 添加一个 R2 bucket binding，
 *      变量名填 R2，选中你的桶。保存后访问
 *      https://<worker名>.<账号>.workers.dev/blog/<文件名>
 *
 *   2. CLI：配置文件里加
 *        [[r2_buckets]]
 *        binding = "R2"
 *        bucket_name = "你的桶名"
 *      然后 wrangler deploy
 *
 * 部署完把 _img/r2.json 的 public_base 改成 https://<worker名>.<账号>.workers.dev
 * 再跑一次 tools/upload-images.py --apply 重新回填即可（不会重复上传）。
 *
 * 免费额度：10 万次请求/天。Worker 内部访问 R2 绑定不计入 subrequest，
 * 也不产生 R2 的 Class B 计费。超出后返回 Error 1027，站点本身照常打开。
 */

// 与 _img/r2.json 的 prefix 保持一致；若你的对象键不带前缀，改成空字符串
const PREFIX = 'blog'

export default {
  async fetch(request, env) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', { status: 405 })
    }

    const key = decodeURIComponent(new URL(request.url).pathname).replace(/^\/+/, '')
    if (!key) {
      return new Response('Not Found', { status: 404 })
    }

    const object = await env.R2.get(PREFIX + key)
    if (object === null) {
      return new Response('Not Found', { status: 404 })
    }

    const headers = new Headers()
    object.writeHttpMetadata(headers)
    headers.set('etag', object.httpEtag)
    if (!headers.has('Cache-Control')) {
      // 文件名里带内容哈希，内容不会变，可以放心长缓存
      headers.set('Cache-Control', 'public, max-age=31536000, immutable')
    }
    // 图片是公开资源，且本站不依赖 Cookie，允许跨域引用
    headers.set('Access-Control-Allow-Origin', '*')

    return new Response(request.method === 'HEAD' ? null : object.body, { headers })
  },
}
