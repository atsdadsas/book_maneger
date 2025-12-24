import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# --- データベースの設定 ---
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- データベースのモデル ---

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), default="不明な著者")
    status = db.Column(db.String(20), default="貸出可能")
    thumbnail = db.Column(db.String(300)) # 画像URL用

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)    # 月〜金
    slot = db.Column(db.Integer, nullable=False)     # 1〜5コマ
    user_name = db.Column(db.String(100), default="予約済み")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    posted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=+9), 'JST')))
    user_ip = db.Column(db.String(50))

# データベースの初期化
    # データベースの初期化部分をこのように一時変更
with app.app_context():
    # 一度すべてのテーブルを削除（これで古い設計図を消去！）
    # db.drop_all()  # ← 初回デプロイ時だけこのコメントアウトを外す
    
    # 新しい設計図（thumbnail入り）で作り直す
    db.create_all()

# --- ルーティング ---

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/index2')
def next_page():
    # ここで templates/index2.html を読み込んでブラウザに送る
    return render_template('index2.html')

@app.route("/status")
def status():
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)
    days = ['月', '火', '水', '木', '金', '土', '日']
    current_day = days[now.weekday()]

    hour = now.hour
    current_slot = 0
    if 9 <= hour < 10: current_slot = 1
    elif 10 <= hour < 12: current_slot = 2
    elif 13 <= hour < 15: current_slot = 3
    elif 15 <= hour < 17: current_slot = 4
    elif 17 <= hour < 19: current_slot = 5

    # 全ての変数が揃ってからDEBUG表示
    print(f"DEBUG: 判定時刻={hour}時, 曜日={current_day}, スロット={current_slot}")

    active_reservation = Reservation.query.filter_by(day=current_day, slot=current_slot).first()

    return render_template('status.html', 
                        res=active_reservation, 
                        day=current_day, 
                        slot=current_slot)

@app.route('/history')
def history():
    all_res = Reservation.query.all()
    res_dict = {(r.day, r.slot): r.user_name for r in all_res}
    return render_template('history.html', reservations=res_dict)

@app.route('/reserve', methods=['POST'])
def reserve():
    day = request.form.get('day')
    slot_raw = request.form.get('slot')
    if not day or not slot_raw:
        return redirect(url_for('history'))

    slot = int(slot_raw)
    existing = Reservation.query.filter_by(day=day, slot=slot).first()
    
    if existing:
        db.session.delete(existing)
    else:
        new_res = Reservation(day=day, slot=slot, user_name="済")
        db.session.add(new_res)
    
    db.session.commit()
    return redirect(url_for('history'))

@app.route('/talk')
def board():
    messages = Post.query.order_by(Post.posted_at.desc()).limit(20).all()
    return render_template('talk.html', messages=messages)

@app.route('/post_message', methods=['POST'])
def post_message():
    content = request.form.get('content')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if content:
        new_post = Post(content=content, user_ip=client_ip)
        db.session.add(new_post)
        db.session.commit()
    
    return redirect(url_for('board'))

@app.route("/add_by_isbn", methods=["POST"])
def add_by_isbn():
    isbn = request.form.get("isbn")
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            image_links = book_info.get("imageLinks", {})
            thumbnail_url = image_links.get("thumbnail")
            
            title = book_info.get("title", "不明なタイトル")
            author_list = book_info.get("authors", ["不明な著者"])
            author = ",".join(author_list)
            
            new_book = Book(
                title=title, 
                author=author, 
                status="貸出可能", 
                thumbnail=thumbnail_url
            )
            db.session.add(new_book)
            db.session.commit()
            return redirect("/")
        return "本が見つかりませんでした", 404
    except Exception as e:
        print(f"ERROR: {e}")
        return f"エラー: {str(e)}", 500

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    book = db.session.get(Book, book_id)
    if book:
        book.status = "貸出中"
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = db.session.get(Book, book_id)
    if book:
        book.status = "貸出可能"
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))