# 📷 TrueNAS Instagram Photo Upload API 安裝指南

> 本指南將協助您在 TrueNAS 系統上安裝和運行 Instagram Photo Upload API 服務。支援多種部署方式，讓您能夠輕鬆管理 Instagram 照片上傳功能。

## 🚀 快速開始

### 系統需求
- TrueNAS SCALE 或 TrueNAS CORE
- Docker 支援
- 至少 1GB 可用磁碟空間
- 網路連線至 Instagram

---

## 📋 方法一：使用 TrueNAS Apps（推薦）

### 步驟 1️⃣：準備專案文件

1. **上傳專案文件**到您的 TrueNAS 系統
2. **建議目錄結構**：
   ```
   /mnt/[您的池名]/apps/instagram-uploader/
   ├── Dockerfile
   ├── docker-compose.yml
   ├── uploads/
   └── [其他專案文件]
   ```

### 步驟 2️⃣：建立 Custom App

1. 登入 **TrueNAS Web 管理界面**
2. 導航至 **Apps** → **Discover Apps**
3. 點選 **Custom App** 按鈕

### 步驟 3️⃣：配置應用程式

| 設定項目 | 配置值 |
|---------|--------|
| **Application Name** | `instagram-uploader` |
| **Image Repository** | `instagram-uploader` |
| **Image Tag** | `latest` |

#### 🔧 環境變數設定
```yaml
IG_EMAIL: example@example.com
IG_PASSWORD: IG_Password
```

#### 🌐 網路配置
| 項目 | 值 |
|------|-----|
| **Container Port** | `5005` |
| **Node Port** | `5005` |
| **Protocol** | `TCP` |

#### 💾 儲存配置
| Host Path | Mount Path |
|-----------|------------|
| `/mnt/[您的池名]/apps/instagram-uploader/uploads` | `/app/uploads` |

### 步驟 4️⃣：建置 Docker Image

```bash
# SSH 連線到 TrueNAS
ssh root@[您的TrueNAS-IP]

# 切換到專案目錄
cd /mnt/[您的池名]/apps/instagram-uploader/

# 建置 Docker Image
docker build -t instagram-uploader .
```

### 步驟 5️⃣：部署應用程式

1. 在 TrueNAS Apps 界面點選 **Install**
2. 等待部署程序完成 ⏳

---

## 🐳 方法二：使用 Docker Compose

### 連線與準備
```bash
# SSH 連線到 TrueNAS
ssh root@[您的TrueNAS-IP]

# 切換到專案目錄
cd /mnt/[您的池名]/apps/instagram-uploader/
```

### 建置與啟動
```bash
# 建置 Docker Image
docker build -t instagram-uploader .

# 使用 Docker Compose 啟動服務
docker-compose up -d
```

### 監控服務狀態
```bash
# 檢查容器狀態
docker-compose ps

# 查看服務日誌
docker-compose logs instagram-uploader

# 實時監控日誌
docker-compose logs -f instagram-uploader
```

---

## ⚡ 方法三：直接使用 Docker 命令

### 建置 Image
```bash
cd /mnt/[您的池名]/apps/instagram-uploader/
docker build -t instagram-uploader .
```

### 運行容器
```bash
docker run -d \
  --name instagram-uploader \
  -p 5005:5005 \
  -e IG_EMAIL="aiko2nd@gmail.com" \
  -e IG_PASSWORD="Abc123456." \
  -v /mnt/[您的池名]/apps/instagram-uploader/uploads:/app/uploads \
  --restart unless-stopped \
  instagram-uploader
```

---

## ✅ 驗證安裝

### 🌐 Web 界面測試
開啟瀏覽器，前往：
```
http://[您的TrueNAS-IP]:5005
```

### 🔧 API 測試
```bash
curl -X POST \
  http://[您的TrueNAS-IP]:5005/upload \
  -F "photo=@/path/to/test/image.jpg" \
  -F "caption=Test upload from TrueNAS! 📸"
```

---

## 🛠️ 容器管理命令

| 操作 | 命令 |
|------|------|
| **查看日誌** | `docker logs instagram-uploader` |
| **停止容器** | `docker stop instagram-uploader` |
| **重新啟動** | `docker restart instagram-uploader` |
| **移除容器** | `docker stop instagram-uploader && docker rm instagram-uploader` |
| **進入容器** | `docker exec -it instagram-uploader /bin/bash` |

---

## ⚠️ 重要注意事項

### 🔐 安全性考量
- **密碼管理**：生產環境建議使用 `.env` 文件管理敏感資訊
- **網路安全**：考慮使用反向代理 (如 Nginx) 加強安全性
- **存取控制**：適當設定防火牆規則

### 🔥 防火牆設定
確保 TrueNAS 防火牆允許 **端口 5005** 的連線：
```bash
# 檢查防火牆狀態
sudo ufw status

# 開放端口（如果需要）
sudo ufw allow 5005
```

### 💾 資料持久性
- **uploads** 目錄已映射到主機
- 容器重啟不會遺失上傳的文件
- 建議定期備份重要資料

### 📊 效能監控
```bash
# 監控容器資源使用
docker stats instagram-uploader

# 檢查磁碟使用量
df -h /mnt/[您的池名]/apps/instagram-uploader/
```

---

## 🆘 故障排除

### 🔍 常見問題診斷

#### ❌ 容器無法啟動
```bash
# 檢查詳細錯誤日誌
docker logs instagram-uploader

# 檢查端口占用情況
netstat -tulpn | grep 5005

# 檢查 Docker 服務狀態
systemctl status docker
```

#### 🌐 無法連接到 Instagram
- ✅ **檢查網路連線**：`ping instagram.com`
- ✅ **驗證帳號密碼**：確認登入資訊正確
- ✅ **處理安全驗證**：可能需要處理 Instagram 雙重驗證

#### 📤 上傳失敗問題
| 檢查項目 | 解決方案 |
|----------|----------|
| **圖片格式** | 支援 JPG, PNG 格式 |
| **檔案大小** | 符合 Instagram 限制（<30MB） |
| **網路連線** | 確保穩定的網路環境 |
| **API 限制** | 避免頻繁請求觸發限制 |

### 📋 除錯日誌分析
```bash
# 查看最近的錯誤日誌
docker logs --tail 50 instagram-uploader | grep -i error

# 監控即時日誌
docker logs -f instagram-uploader
```

---

## 📞 技術支援

如遇到問題，請提供以下資訊：
- TrueNAS 版本
- Docker 版本
- 錯誤日誌內容
- 網路環境描述

---

*🎉 安裝完成後，您就可以開始使用 Instagram Photo Upload API 服務了！*
