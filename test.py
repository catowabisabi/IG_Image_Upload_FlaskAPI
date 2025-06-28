import requests
import io
import os
from urllib.parse import urlparse

# API endpoint
api_url = "http://192.168.0.200:5005/upload"

# Instagram 憑證 - 請修改為您的實際帳號密碼
ig_email = "aiko2nd@gmail.com"     # 您的 Instagram 帳號
ig_password = "Abc123456."         # 您的 Instagram 密碼

# Image URL to download
image_url = "https://static-cse.canva.com/blob/1648460/feature_photo-to-anime_promo-showcase_01-AFTER.jpg"

print("正在下載圖片...")
try:
    # Download the image as binary data
    image_response = requests.get(image_url)
    image_response.raise_for_status()  # Raise an exception for bad status codes
    
    # Get binary data
    image_binary = image_response.content
    print(f"圖片已下載，大小: {len(image_binary)} bytes")
    
    # Get filename from URL for the upload
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path) or "temp_image.jpg"
    
    # Create a file-like object from binary data
    image_file = io.BytesIO(image_binary)
    
    # Now upload to Instagram API using binary data with credentials
    print("正在上傳到 Instagram...")
    files = {'photo': (filename, image_file, 'image/jpeg')}
    data = {
        'caption': 'Hello from TrueNAS! 二進制數據測試上傳',
        'ig_email': ig_email,
        'ig_password': ig_password
    }
    print("正在發送請求...")
    response = requests.post(api_url, files=files, data=data)
    print("API 回應:", response.json())
    print("狀態碼:", response.status_code)
    
    if response.status_code == 200:
        print("✅ 上傳成功！")
    else:
        print("❌ 上傳失敗")
    
    # Close the BytesIO object
    image_file.close()
    
except requests.exceptions.RequestException as e:
    print(f"下載圖片時出錯: {e}")
except Exception as e:
    print(f"發生錯誤: {e}")