import requests
import os
import io

# API endpoint
api_url = "http://192.168.0.200:5005/upload"

# 請將這裡改為您本地圖片的路徑
image_path = "https://static-cse.canva.com/blob/1648460/feature_photo-to-anime_promo-showcase_01-AFTER.jpg"  # 請修改為實際的圖片路徑

# Instagram 憑證 - 請修改為您的實際帳號密碼
ig_email = "aiko2nd@gmail.com"     # 請修改為您的 Instagram 帳號
ig_password = "Abc123456."           # 請修改為您的 Instagram 密碼

# 檢查文件是否存在
if not os.path.exists(image_path):
    print(f"錯誤: 找不到圖片文件 {image_path}")
    print("請將 image_path 變數改為您實際的圖片路徑")
    exit(1)

# 檢查是否設置了 Instagram 憑證
if ig_email == "your_email@example.com" or ig_password == "your_password":
    print("錯誤: 請在測試文件中設置您的 Instagram 帳號和密碼")
    print("請修改 ig_email 和 ig_password 變數")
    exit(1)

print(f"正在讀取圖片: {image_path}")

try:
    # Read the image as binary data
    with open(image_path, 'rb') as f:
        image_binary = f.read()
    
    print(f"圖片已讀取，大小: {len(image_binary)} bytes")
    
    # Create a file-like object from binary data
    image_file = io.BytesIO(image_binary)
    
    # Get filename for upload
    filename = os.path.basename(image_path)
    
    print("正在上傳到 Instagram...")
    
    # Upload using binary data with Instagram credentials
    files = {'photo': (filename, image_file, 'image/jpeg')}
    data = {
        'caption': 'Hello from TrueNAS! 本地二進制數據測試上傳',
        'ig_email': ig_email,
        'ig_password': ig_password
    }
    
    response = requests.post(api_url, files=files, data=data)
    
    print("API 回應:", response.json())
    print("狀態碼:", response.status_code)
    
    if response.status_code == 200:
        print("✅ 上傳成功！")
    else:
        print("❌ 上傳失敗")
    
    # Close the BytesIO object
    image_file.close()
        
except FileNotFoundError:
    print(f"錯誤: 找不到文件 {image_path}")
except Exception as e:
    print(f"發生錯誤: {e}") 