# Bilibili‑Daily‑Sign 🎫  

自动领取 B 站大会员每日赠送的10经验，需要每天至少播放一个视频，基于 **GitHub Actions + Selenium**。  
每天 23:00 (UTC +8) 定时执行，支持手动触发。

> **⚠️ 隐私声明**  
> 本仓库不保存任何 Cookie / 邮箱口令。  
> 你必须在自己的 Fork 中添加 Secrets 才能正常运行。  
> **切勿** 把 Cookie 直接写进代码或 Issue！

---

## ✨ 功能特性
- 一键部署到 GitHub Actions，完全免服务器
- 领取结果通过邮件通知（成功 / 已领取 / 失败）

---

## 🚀 快速开始（5 步完成）

1. **Fork 本仓库**

2. **获取 B 站 Cookie**  
   - 浏览器登录 https://account.bilibili.com/big  
   - 打开 DevTools(F12) → Application → Cookies → `SESSDATA`、`bili_jct` 等  
   - 将 Cookie 转写成 JSON 格式，如：  
     ```js
    [
  {
    "name": "SESSDATA",
    "value": "<你的SESSDATA值>",
    "domain": ".bilibili.com",
    "path": "/"
  },
  {
    "name": "bili_jct",
    "value": "<你的bili_jct值>",
    "domain": ".bilibili.com",
    "path": "/"
  },
   ```
   - 删去JSON中所有空格和换行，压缩成一行的的形式
   
   3. **添加 Secrets**  
   在你的仓库 *Settings → Secrets and variables → Actions - Repository secerts* 中依次创建：  

   | Name | 示例值 | 说明 |
   |------|--------|------|
   | `BILIBILI_COOKIES` | `[{"name":"SESSDATA","value":"xxx",...}]` | 必填 |
   | `SMTP_HOST` | `smtp.qq.com` | 必填 |
   | `SMTP_PORT` | `465` | 必填 |
   | `SENDER_EMAIL` | `123456@qq.com` | 必填 |
   | `SENDER_PASSWORD` | `qq‑授权码` | 必填 |
   | `RECEIVER_EMAIL` | `123456@qq.com` | 可与发件人相同 |

4. **启用 GitHub Actions**  
   第一次 Fork 后，进入 **Actions** 标签页，点击 **“I understand…”** 以启用工作流。

5. **检查运行结果**  
   - 等待下一次定时任务，或在 **Actions → Bilibili Daily Sign → Run workflow** 手动触发  
   - 成功后会收到邮件；也可在 Job 日志里查看「领取成功」字样。
