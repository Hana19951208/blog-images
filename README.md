# 🖼️ Blog Images Box

个人博客专属图床项目，集成图片自动压缩、CDN 预热以及每日壁纸自动存档功能。

## ✨ 特性

- **自动压缩**：利用 GitHub Actions 对上传的图片进行无损/近无损压缩，优化访问速度并节省流量。
- **针对性预热**：仅对本次新增或修改的图片进行预热，避免全量扫描，提高效率。
- **并发控制**：内置并发冲突防护，确保多图连续上传时的 Git 提交安全。
- **CDN 预热**：图片压缩提交后，自动请求 CDN 节点触发缓存。
- **自动化存档**：集成 Bing 和 Unsplash 每日壁纸自动抓取与分类存档。
- **结构化存储**：按照日期和来源清晰组织图片目录，方便管理和直接引用。

## 📂 目录结构

```text
.
├── .github/workflows/      # GitHub Actions 自动化流水线
├── blog/                   # 通用博客图片存储（按日期分类）
│   └── 2026-01/
├── wallpapers/             # 壁纸存档
│   ├── bing/               # 必应每日壁纸（包含 meta.json 和故事）
│   └── unsplash/           # Unsplash 精选壁纸
└── README.md
```

## 🚀 自动化流程

项目托管于 GitHub，通过 `.github/workflows/compress-images.yml` 驱动：

1. **触发条件**：推送图片或手动触发（处理最近一次提交内容）。支持并发控制，防止 Git 冲突。
2. **精准过滤**：通过 `git diff` 仅提取本次变动的图片，排除已删除的文件。
3. **针对性压缩**：使用 `calibreapp/image-actions` 配合 `compressOnly` 模式进行压缩。
4. **自动回写**：压缩后的图片自动提交回仓库，仅限图片文件变动。
5. **CDN 预热**：
   - 等待 GitHub 节点同步（10s 延迟）。
   - 依次请求 `https://{CDN_DOMAIN}/{path}` 触发 CDN 缓存。
   - 实时输出预热结果（✅ 成功 / ❌ 失败）。

## 🛠️ 配置说明

### GitHub Secrets / Variables

- `GITHUB_TOKEN`: 默认提供。
- `CDN_DOMAIN` (Optional): CDN 访问域名。在 **Settings -> Secrets -> Actions** 中配置，默认回退为 `img.fangenwu.cn`。



## 📝 调试与志

我们在 Workflow 中增加了详细的日志输出，您可以在 GitHub Actions 的运行日志中查看：
- **[日志]**: 流程开始与结束。
- **[信息]**: 发现的待处理图片列表。
- **[调试]**: 单个图片的预热全路径及响应状态码。


---

**Proudly powered by GitHub Actions & Cloudflare.**
