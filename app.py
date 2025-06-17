from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Tạo database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            image_url TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

#  API thêm bài viết
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    image_url = data.get('image_url')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO posts (name, content, image_url, date) VALUES (?, ?, ?, ?)',
        (name, content, image_url, date)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Post created successfully'}), 201

#  API lấy danh sách bài viết
@app.route('/posts', methods=['GET'])
def get_posts():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    conn.close()

    post_list = []
    for post in posts:
        post_list.append({
            'id': post[0],
            'name': post[1],
            'content': post[2],
            'image_url': post[3],
            'date': post[4]
        })
    
    return jsonify(post_list), 200

#  Chạy server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
