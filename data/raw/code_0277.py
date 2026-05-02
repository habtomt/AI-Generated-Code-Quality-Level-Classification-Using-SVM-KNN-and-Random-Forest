import sqlite3
import os
import hashlib
from datetime import datetime

class VideoSystem:
    def __init__(self, db_name="platform.db", upload_folder="user_videos"):
        self.db_name = db_name
        self.upload_folder = upload_folder
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                password_hash TEXT,
                                role TEXT DEFAULT 'user')''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                title TEXT,
                                file_path TEXT,
                                status TEXT DEFAULT 'pending',
                                created_at TIMESTAMP,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')
            conn.commit()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, role='user'):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                               (username, self._hash_password(password), role))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def upload_video(self, username, title, source_path):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                filename = f"{user_id}_{int(datetime.now().timestamp())}_{os.path.basename(source_path)}"
                dest_path = os.path.join(self.upload_folder, filename)
                
                # In a real app, use shutil.copy or a file upload handler
                with open(source_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())

                cursor.execute("""INSERT INTO videos (user_id, title, file_path, created_at) 
                                  VALUES (?, ?, ?, ?)""", 
                               (user_id, title, dest_path, datetime.now()))
                conn.commit()
                return True
        return False

    def moderate_video(self, admin_username, video_id, approve=True):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ?", (admin_username,))
            user = cursor.fetchone()
            
            if user and user[0] == 'admin':
                status = 'approved' if approve else 'rejected'
                cursor.execute("UPDATE videos SET status = ? WHERE id = ?", (status, video_id))
                conn.commit()
                return True
        return False

    def get_feed(self, include_pending=False):
        query = "SELECT videos.title, users.username, videos.status FROM videos JOIN users ON videos.user_id = users.id"
        if not include_pending:
            query += " WHERE videos.status = 'approved'"
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

if __name__ == "__main__":
    system = VideoSystem()
    
    # Setup Admin and User
    system.create_user("admin_root", "secure123", role="admin")
    system.create_user("dev_junior", "python4life")
    
    # Mock Workflow
    # system.upload_video("dev_junior", "My First Code", "local_file.mp4")
    # system.moderate_video("admin_root", 1, approve=True)
    # print(system.get_feed())