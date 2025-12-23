import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime,timedelta,timezone

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

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)    # 月〜金
    slot = db.Column(db.Integer, nullable=False)     # 1〜5コマ
    user_name = db.Column(db.String(100), default="予約済み")

with app.app_context():
    db.create_all()

# --- ルーティング ---

@app.route("/status")
def status():
    now= datetime.now()
# ★ 日本時間(JST)を設定する
    jst = timezone(timedelta(hours=+9), 'JST')
    # ★ UTCではなく日本時間で取得する
    now = datetime.now(jst)
    
# 2. 曜日を日本語に変換 (0=月, 1=火...)
    days=['月', '火', '水', '木', '金', '土', '日']
    # 火曜日ならnow.weekday=1 days[1]=火
    current_day=days[now.weekday()]
# 3. 現在の時間から「何コマ目」かを判定（例）
    hour = now.hour
    current_slot = 0
    if 9 <= hour < 10: current_slot = 1
    elif 10 <= hour < 12: current_slot = 2
    elif 13 <= hour < 15: current_slot = 3
    elif 15 <= hour < 17: current_slot = 4
    elif 17 <= hour < 19: current_slot = 5

    active_reservation = Reservation.query.filter_by(day=current_day, slot=current_slot).first()

    return render_template('status.html', 
                        res=active_reservation, 
                        day=current_day, 
                        slot=current_slot)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/history')
def history():
    # データベースから全予約を取得して辞書に変換
    all_res = Reservation.query.all()
    # 曜日は文字列、スロットは整数として辞書のキーにする
    res_dict = {(r.day, r.slot): r.user_name for r in all_res}
    return render_template('history.html', reservations=res_dict)

@app.route('/reserve', methods=['POST'])
def reserve():
    day = request.form.get('day')
    slot = int(request.form.get('slot'))
    
    # 既に予約があるかデータベースを確認
    existing = Reservation.query.filter_by(day=day, slot=slot).first()
    
    if existing:
        # 予約がある場合は「キャンセル」
        db.session.delete(existing)
    else:
        # 予約がない場合は「新規登録」
        new_res = Reservation(day=day, slot=slot)
        db.session.add(new_res)
    
    db.session.commit()
    return redirect(url_for('history'))

# --- 蔵書管理系 ---
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
        return "本が見つかりませんでした", 404
    except Exception as e:
        return f"エラー: {str(e)}", 500

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