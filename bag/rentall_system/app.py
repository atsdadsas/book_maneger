import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# --- データベースの設定 ---
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- データベースのモデル ---

# 既存の本のモデル
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), default="不明な著者")
    status = db.Column(db.String(20), default="貸出可能")

# 【追加】予約情報のモデル
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)    # 月〜金
    slot = db.Column(db.Integer, nullable=False)   # 1〜5コマ
    user_name = db.Column(db.String(100), default="予約済み")

# データベースの初期化
with app.app_context():
    db.create_all()

# --- ルーティング ---

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# 【追加】予約ページを表示する
@app.route('/history')
def history():
    # 全ての予約データを取得
    all_res = Reservation.query.all()
    # HTMLで扱いやすいように辞書型に変換 {(曜日, コマ): 名前}
    res_dict = {(r.day, r.slot): r.user_name for r in all_res}
    return render_template('history.html', reservations=res_dict)

# 【追加】予約を実行する
@app.route('/reserve', methods=['POST'])
def reserve():
    day = request.form.get('day')
    slot = int(request.form.get('slot'))
    user_name = request.form.get('user_name') or "利用者"

    # 既に予約があるか確認
    existing = Reservation.query.filter_by(day=day, slot=slot).first()
    if existing:
        # 既にある場合は削除（キャンセル機能）
        db.session.delete(existing)
    else:
        # 新しく予約を追加
        new_res = Reservation(day=day, slot=slot, user_name=user_name)
        db.session.add(new_res)
    
    db.session.commit()
    return redirect(url_for('history'))

# --- 以下、既存の蔵書管理系ルーティング ---
@app.route("/add_by_isbn", methods=["POST"])
def add_by_isbn():
    isbn = request.form.get("isbn")
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            title = book_info.get("title", "不明なタイトル")
            author_list = book_info.get("authors", ["不明な著者"])
            author = ",".join(author_list)
            new_book = Book(title=title, author=author, status="蔵書")
            db.session.add(new_book)
            db.session.commit()
            return redirect("/")
        else:
            return "本が見つかりませんでした", 404
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('book_name')
    if title:
        new_book = Book(title=title)
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))