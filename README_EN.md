# 🖼️ Blog Images Box (V2.0)

[![GitHub Stars](https://img.shields.io/github/stars/Hana19951208/blog-images?style=flat-square)](https://github.com/Hana19951208/blog-images/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Hana19951208/blog-images?style=flat-square)](https://github.com/Hana19951208/blog-images/network/members)
[![License](https://img.shields.io/github/license/Hana19951208/blog-images?style=flat-square)](https://github.com/Hana19951208/blog-images/blob/main/LICENSE)

> **The ultimate elegant image hosting solution.** Integrated with Typora + PicGo + GitHub Actions + WeChat Official Account Sync.
> Auto-compression, efficient preheating, and idempotent synchronization for seamless asset distribution.

[English说明] | [中文说明](./README.md)

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

## 🛠️ Local Debugging

```bash
# Copy and configure env
cp .env.example .env
# Run sync test
python3 scripts/sync_to_wechat.py "blog/test.jpg"
```

---

**Proudly powered by GitHub Actions & Cloudflare.**
If you like it, please give a ⭐️!
