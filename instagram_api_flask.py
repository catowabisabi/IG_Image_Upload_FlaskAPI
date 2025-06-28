import os
import time
import uuid
from flask import Flask, request, jsonify
from instagrapi import Client
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['SESSION_FOLDER'] = os.path.join(os.getcwd(), 'sessions')

# 確保 session 目錄存在
os.makedirs(app.config['SESSION_FOLDER'], exist_ok=True)

class InstagramApi:
    def __init__(self, ig_email, ig_password):
        if not ig_email or not ig_password:
            raise ValueError("請提供有效的 Instagram 帳號和密碼")
        
        self.api_client = Client()
        self.ig_email = ig_email
        self.session_file = os.path.join(app.config['SESSION_FOLDER'], f"{ig_email}.json")
        
        try:
            # 嘗試載入現有的 session
            if os.path.exists(self.session_file):
                print(f"找到現有 session: {self.session_file}")
                try:
                    self.api_client.load_settings(self.session_file)
                    # 驗證 session 是否有效
                    self.api_client.get_timeline_feed()
                    print(f"成功使用現有 session: Email: {ig_email}")
                    return
                except Exception as e:
                    print(f"Session 已過期或無效，需要重新登入: {e}")
            
            # 如果沒有 session 或 session 無效，執行新登入
            self.api_client.login(ig_email, ig_password)
            # 保存新的 session
            self.api_client.dump_settings(self.session_file)
            print(f"InstagramApi 初始化成功並保存 session: Email: {ig_email}")
        except Exception as e:
            print(f"登入失敗: {e}")
            raise

    def upload_photo(self, image_path: str, ig_text: str):
        try:
            self.api_client.photo_upload(path=image_path, caption=ig_text)
            print("照片上傳成功")
            # The original 20-second sleep remains.
            time.sleep(20)
            return True, "上傳成功"
        except Exception as e:
            print(f"上傳過程中發生錯誤: {e}")
            return False, str(e)

@app.route('/upload', methods=['POST'])
def upload_file_to_instagram():
    # 檢查是否有照片
    if 'photo' not in request.files:
        return jsonify({"error": "請求中沒有照片"}), 400
    
    # 檢查是否提供了 Instagram 憑證
    ig_email = request.form.get('ig_email')
    ig_password = request.form.get('ig_password')
    
    if not ig_email or not ig_password:
        return jsonify({"error": "請提供 Instagram 帳號 (ig_email) 和密碼 (ig_password)"}), 400
    
    file = request.files['photo']
    caption = request.form.get('caption', '')

    if file.filename == '':
        return jsonify({"error": "沒有選擇文件"}), 400

    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            # 保存文件
            file.save(filepath)
            
            # 創建 Instagram API 實例
            instagram_api = InstagramApi(ig_email, ig_password)
            
            # 上傳照片
            success, message = instagram_api.upload_photo(filepath, caption)
            
        except ValueError as e:
            # Instagram 登入錯誤
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            # 其他錯誤
            return jsonify({"error": f"發生錯誤: {str(e)}"}), 500
        finally:
            # 清理臨時文件
            if os.path.exists(filepath):
                os.remove(filepath)

        if success:
            return jsonify({"message": "照片上傳成功"}), 200
        else:
            return jsonify({"error": f"照片上傳失敗: {message}"}), 500
    
    return jsonify({"error": "發生未知錯誤"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)