# TrueNAS 安裝指南 - Instagram Photo Upload API

本指南將協助您在 TrueNAS 上安裝和運行 Instagram Photo Upload API。

## 方法一：使用 TrueNAS Apps (推薦)

### 步驟 1：準備文件
1. 將所有專案文件上傳到您的 TrueNAS 系統
2. 建議放在 `/mnt/[您的池名]/apps/instagram-uploader/` 目錄下

### 步驟 2：在 TrueNAS 中建立 Custom App
1. 登入 TrueNAS Web 界面
2. 前往 **Apps** > **Discover Apps**
3. 點選 **Custom App**

### 步驟 3：配置 Custom App
填入以下資訊：

**Application Name:** `instagram-uploader`

**Container Images:**
- **Image repository:** `instagram-uploader` (本地建置)
- **Image tag:** `latest`

**Container Configuration:**
- **Container Args:** 留空
- **Container Environment Variables:**
  - `IG_EMAIL`: `aiko2nd@gmail.com`
  - `IG_PASSWORD`: `Abc123456.`

**Networking:**
- **Port Forwarding:**
  - **Container Port:** `5005`
  - **Node Port:** `5005`
  - **Protocol:** `TCP`

**Storage:**
- **Host Path Volumes:**
  - **Host Path:** `/mnt/[您的池名]/apps/instagram-uploader/uploads`
  - **Mount Path:** `/app/uploads`

### 步驟 4：建置 Docker Image
在部署前，您需要先建置 Docker image：

1. SSH 連線到您的 TrueNAS 系統
2. 切換到專案目錄：
   ```bash
   cd /mnt/[您的池名]/apps/instagram-uploader/
   ```
3. 建置 Docker image：
   ```bash
   docker build -t instagram-uploader .
   ```

### 步驟 5：部署應用程式
1. 在 TrueNAS Apps 界面中點選 **Install**
2. 等待部署完成

## 方法二：使用 Docker Compose

### 步驟 1：SSH 連線到 TrueNAS
```bash
ssh root@[您的TrueNAS IP]
```

### 步驟 2：切換到專案目錄
```bash
cd /mnt/[您的池名]/apps/instagram-uploader/
```

### 步驟 3：建置和啟動
```bash
# 建置 image
docker build -t instagram-uploader .

# 使用 docker-compose 啟動
docker-compose up -d
```

### 步驟 4：檢查狀態
```bash
docker-compose ps
docker-compose logs instagram-uploader
```

## 方法三：直接使用 Docker 命令

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

## 驗證安裝

1. 開啟瀏覽器，前往 `http://[您的TrueNAS IP]:5005`
2. 使用以下命令測試 API：
   ```bash
   curl -X POST \
     http://[您的TrueNAS IP]:5005/upload \
     -F "photo=@/path/to/test/image.jpg" \
     -F "caption=Test upload from TrueNAS!"
   ```

## 管理容器

### 查看日誌
```bash
docker logs instagram-uploader
```

### 停止容器
```bash
docker stop instagram-uploader
```

### 重新啟動容器
```bash
docker restart instagram-uploader
```

### 移除容器
```bash
docker stop instagram-uploader
docker rm instagram-uploader
```

## 注意事項

1. **安全性：** 您的 Instagram 密碼已硬編碼在配置中。建議在生產環境中使用環境變數文件 (.env) 來管理敏感資訊。

2. **防火牆：** 確保 TrueNAS 防火牆允許端口 5005 的連線。

3. **資料持久性：** uploads 目錄已映射到主機，確保上傳的文件不會因容器重啟而丟失。

4. **資源監控：** 定期檢查容器的資源使用情況，特別是在高頻率使用時。

## 故障排除

### 常見問題

1. **容器無法啟動：**
   - 檢查 Docker 日誌：`docker logs instagram-uploader`
   - 確認端口 5005 沒有被其他服務占用

2. **無法連接到 Instagram：**
   - 檢查網路連線
   - 確認 Instagram 帳號密碼正確
   - 可能需要處理 Instagram 的安全驗證

3. **上傳失敗：**
   - 檢查圖片格式是否支援
   - 確認檔案大小符合 Instagram 限制
   - 查看應用程式日誌了解詳細錯誤訊息 