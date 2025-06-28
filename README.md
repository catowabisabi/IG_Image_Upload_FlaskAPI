# Instagram Upload API Service / Instagram 上傳 API 服務

[English](#english) | [中文](#中文)

## English

### Description
A Flask-based API service that handles Instagram photo uploads. It provides a simple REST API endpoint for uploading photos to Instagram, with session management to maintain login states.

### Features
- Photo upload to Instagram via API
- Session management for login persistence
- Docker support for easy deployment
- Secure file handling
- Rate limiting protection

### Installation

#### Using Docker (Recommended)
```bash
# Build the Docker image
docker build -t ig_flask_app .

# Run the container
docker run -d --name ig_flask_container -p 5000:5000 -p 5005:5005 ig_flask_app
```

#### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python instagram_api_flask.py
```

### API Usage
Upload a photo to Instagram:
```bash
curl -X POST http://localhost:5005/upload \
  -F "photo=@/path/to/photo.jpg" \
  -F "ig_email=your_email@example.com" \
  -F "ig_password=your_password" \
  -F "caption=Your photo caption"
```

### Notes
- The service maintains session files to reduce login frequency
- Uploaded files are temporarily stored and then automatically deleted
- Rate limiting is implemented to prevent API abuse

---

## 中文

### 描述
基於 Flask 的 Instagram 照片上傳 API 服務。提供簡單的 REST API 端點用於上傳照片到 Instagram，並具有會話管理功能以維持登入狀態。

### 功能特點
- 通過 API 上傳照片到 Instagram
- 會話管理實現登入持久化
- 支援 Docker 部署
- 安全的檔案處理
- 請求頻率限制保護

### 安裝方法

#### 使用 Docker（推薦）
```bash
# 建立 Docker 映像檔
docker build -t ig_flask_app .

# 執行容器
docker run -d --name ig_flask_container -p 5000:5000 -p 5005:5005 ig_flask_app
```

#### 手動安裝
```bash
# 安裝依賴
pip install -r requirements.txt

# 執行應用
python instagram_api_flask.py
```

### API 使用方法
上傳照片到 Instagram：
```bash
curl -X POST http://localhost:5005/upload \
  -F "photo=@/path/to/photo.jpg" \
  -F "ig_email=your_email@example.com" \
  -F "ig_password=your_password" \
  -F "caption=Your photo caption"
```

### 注意事項
- 服務會保存會話檔案以減少登入次數
- 上傳的檔案會暫時儲存後自動刪除
- 實作了請求頻率限制以防止濫用 API 