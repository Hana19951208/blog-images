# 🖼️ Blog Images Box (V2.0)

<p align="center">
  <img src="https://img.shields.io/github/stars/Hana19951208/blog-images?style=for-the-badge&logo=github&color=5e5ce6" alt="Stars">
  <img src="https://img.shields.io/github/forks/Hana19951208/blog-images?style=for-the-badge&logo=github&color=5e5ce6" alt="Forks">
  <img src="https://img.shields.io/github/license/Hana19951208/blog-images?style=for-the-badge&logo=github&color=5e5ce6" alt="License">
  <br>
  <img src="https://img.shields.io/github/last-commit/Hana19951208/blog-images?style=flat-square" alt="Last Commit">
  <img src="https://img.shields.io/github/v/tag/Hana19951208/blog-images?style=flat-square&label=release" alt="Release">
</p>

> **The ultimate elegant image hosting solution.** Integrated with Typora + PicGo + GitHub Actions + WeChat Official Account Sync.
> Auto-compression, efficient preheating, and idempotent synchronization for seamless asset distribution.

[English说明] | [中文说明](./README.md)

---

## 🌐 Documentation Hub
This project and related tools are accessible via a unified domain:
- **Image Hosting Box**: [docs.fangenwu.cn/BlogImagesBox](https://docs.fangenwu.cn/BlogImagesBox)
- **Daily Wallpaper Hub**: [docs.fangenwu.cn/DailyWallpaperHub](https://docs.fangenwu.cn/DailyWallpaperHub)

---

## 💡 Why this? (Solving the Pain Points)


As a blogger or developer, are you tired of these hurdles?
- ❌ **Oversized Images**: Manual compression is tedious; uncompressed assets bloat CDN costs.
- ❌ **Tedious Sync**: Uploading to GitHub is one thing, but manually uploading again for WeChat is another.
- ❌ **Slow Access**: GitHub Raw is unstable; manual cache purging/preheating is annoying.
- ❌ **IP Restrictions**: WeChat APIs use strict IP whitelists; GitHub Actions' dynamic IPs are unusable.

**Blog Images Box** is built to tackle these once and for all! 🚀

---

## ✨ Core Features

- ⚡ **Parallel Job Pipeline**: CDN Preheat (Fast) vs. Compression & Sync (Background) runs in parallel, 200% faster.
- 📦 **Typora + PicGo Integration**: Screenshot, paste, and let GitHub handle the rest.
- 📉 **Smart Incremental Compression**: Using `jpegoptim` / `optipng` on *new/modified files only*, reducing size by 60%+.
- 📲 **Automated WeChat Sync**: Circumvents WeChat IP whitelists using a bridge server (e.g., Tencent Cloud).
- 🛡️ **Security-First Architecture**: Dedicated `github-bot` user support to avoid security alerts and safeguard root access.
- 🔄 **Idempotent Sync (Registry)**: Built-in MD5 check prevents duplicate uploads and saves WeChat material quota.
- 📁 **Daily Wallpaper Archive**: Auto-collects Bing/Unsplash daily wallpapers.

---

## 📁 Directory Structure

```text
.
├── .github/workflows/      # 🚀 Professional Parallel Workflows
├── blog/                   # 📷 Image Storage (Typora default folder)
├── wallpapers/             # 🎨 Wallpaper Archives
├── scripts/                # 🐍 Core Logic (Python)
└── docs/                   # 📄 Static Docs for GitHub Pages
```

---

## 🚀 Quick Start

### 1. Basic Setup
1. **Fork** this repo.
2. Configure **Typora + PicGo** (GitHub plugin) to point to your repo.

### 2. Configure GitHub Secrets
Go to **Settings -> Secrets -> Actions** and add:

| Secret Name | Meaning | Description |
| :--- | :--- | :--- |
| `CDN_DOMAIN` | CDN Domain | e.g., `img.example.com` |
| `WECHAT_APP_ID` | WeChat AppID | Found in WeChat Backend |
| `WECHAT_APP_SECRET`| WeChat AppSecret| Found in WeChat Backend |
| `SERVER_HOST` | Bridge Server IP | Your fixed IP server |
| `SERVER_USER` | SSH Username | **Recommended: `github-bot`** |
| `SERVER_KEY` | SSH Private Key | PEM format private key content |

---

## 🛡️ Security Hardening (Recommended)

To prevent login alerts on your server due to GitHub Actions' global nodes, we recommend:

1. **Create Dedicated User**:
   ```bash
   # On your server
   adduser github-bot
   ```
2. **Restrict Access**:
   Limit this user to `~/blog-sync` directory only.
3. **Deploy Keys**:
   Follow the SSH Key tutorial below for the `github-bot` user.
4. **Whitelist User**:
   In your cloud console (e.g., Tencent Cloud Center), whitelist `github-bot` from login alerts. Even if triggered from the US or Singapore, it's safe and isolated.

---

## 🔑 SSH Key Setup Tutorial

1. **Generate PEM Format Key** (Highest compatibility):
   ```bash
   ssh-keygen -t rsa -b 4096 -m PEM -f ./id_rsa_github -N ""
   ```
2. **Deploy Public Key**:
   ```bash
   ssh-copy-id -i ./id_rsa_github.pub github-bot@YOUR_SERVER_IP
   ```
3. **Local Verification**:
   ```bash
   ssh -i ./id_rsa_github github-bot@YOUR_SERVER_IP
   ```

---

## 🌐 Advanced: Cloudflare Worker Acceleration (Recommended)

GitHub Raw access can be unstable in some regions. Using Cloudflare Worker, you can transform it into a powerful gateway with **global CDN caching, no-ICP-filing requirement, and custom domain support**.

### 1. Create a Worker
1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/) and go to **Workers & Pages**.
2. Click **Create application** -> **Create Worker**.
3. Name it `blog-images-proxy` and paste the provided code into the editor.

### 2. Implementation Code
Update the following variables with your repo info:
```js
const GITHUB_USER = 'hana19951208';
const GITHUB_REPO = 'BlogImagesBox';
const GITHUB_BRANCH = 'main';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const githubUrl = `https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/${GITHUB_BRANCH}${path}`;
    
    let response = await fetch(githubUrl, {
      headers: { 'User-Agent': 'Cloudflare-Worker' }
    });

    if (response.status === 200) {
      let newHeaders = new Headers(response.headers);
      newHeaders.delete("Vary");
      newHeaders.delete("X-Frame-Options");
      newHeaders.delete("Content-Security-Policy");
      // Cache for 1 year for maximum speed
      newHeaders.set("Cache-Control", "public, max-age=31536000, s-maxage=31536000, immutable");
      newHeaders.set("access-control-allow-origin", "*");
      return new Response(response.body, { status: 200, headers: newHeaders });
    }
    return response;
  }
}
```

### 3. Bind Custom Domain
1. In the Worker dashboard, click **Settings** -> **Triggers** -> **Custom Domains**.
2. Add your domain (e.g., `img.fangenwu.cn`).
3. **Note**: If your domain is still under ICP verification, ensure your nameservers are pointed to Cloudflare.

---

## 🎨 Using with Typora + PicGo

1. Select **GitHub** in PicGo settings.
2. **Set Custom Domain**: Enter your Cloudflare Worker URL (e.g., `https://img.fangenwu.cn`).
3. Now, when you paste images in Typora, PicGo will upload them to GitHub and return the Cloudflare-accelerated URL.

---


**Proudly powered by GitHub Actions & Cloudflare.**
If you like it, please give a ⭐️!
