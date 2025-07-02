import os
import time
import uuid
from flask import Flask, request, jsonify
from instagrapi import Client
from werkzeug.utils import secure_filename
from typing import Dict, Tuple, Optional

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

class SessionManager:
    _instances: Dict[str, 'InstagramApi'] = {}
    
    @classmethod
    def get_instance(cls, ig_email: str, ig_password: str) -> 'InstagramApi':
        if ig_email not in cls._instances:
            cls._instances[ig_email] = InstagramApi(ig_email, ig_password)
        return cls._instances[ig_email]
    
    @classmethod
    def remove_instance(cls, ig_email: str):
        if ig_email in cls._instances:
            del cls._instances[ig_email]

class InstagramApi:
    def __init__(self, ig_email: str, ig_password: str):
        if not ig_email or not ig_password:
            raise ValueError("請提供有效的 Instagram 帳號和密碼")
        
        self.ig_email = ig_email
        self.ig_password = ig_password
        self.api_client = Client()
        self._login()
        
    def _login(self):
        try:
            self.api_client.login(self.ig_email, self.ig_password)
            print(f"InstagramApi 初始化成功: Email: {self.ig_email}")
        except Exception as e:
            print(f"登入失敗: {e}")
            # 確保失敗的實例被移除
            SessionManager.remove_instance(self.ig_email)
            raise

    def _handle_session_error(self, func):
        try:
            return func()
        except Exception as e:
            if "login_required" in str(e).lower() or "login again" in str(e).lower():
                print(f"Session 已失效，重新登入: {self.ig_email}")
                self._login()
                return func()
            raise

    def upload_photo(self, image_path: str, ig_text: str) -> Tuple[bool, str]:
        try:
            def upload():
                self.api_client.photo_upload(path=image_path, caption=ig_text)
                print("照片上傳成功")
                time.sleep(20)
                return True, "上傳成功"
                
            return self._handle_session_error(upload)
        except Exception as e:
            print(f"上傳過程中發生錯誤: {e}")
            return False, str(e)

@app.route('/upload', methods=['POST'])
def upload_file_to_instagram():
    if 'photo' not in request.files:
        return jsonify({"error": "請求中沒有照片"}), 400
    
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
            file.save(filepath)
            
            # 使用 SessionManager 獲取或創建 Instagram API 實例
            instagram_api = SessionManager.get_instance(ig_email, ig_password)
            
            success, message = instagram_api.upload_photo(filepath, caption)
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            return jsonify({"error": f"發生錯誤: {str(e)}"}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        if success:
            return jsonify({"message": "照片上傳成功"}), 200
        else:
            return jsonify({"error": f"照片上傳失敗: {message}"}), 500
    
    return jsonify({"error": "發生未知錯誤"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)