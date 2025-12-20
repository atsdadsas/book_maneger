from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import os  # OS環境変数を使用するために必要

app = Flask(__name__)

# --- データベースの設定 ---
# Renderの環境変数 DATABASE_URL があれば優先、なければローカルの SQLite を使用
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    # SQLAlchemy 1.4以降、postgres:// ではなく postgresql:// が必須
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- データベースのモデル ---
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # ISBN追加時に著者名も保存できるよう項目を追加
    author = db.Column(db.String(100), default="不明な著者")
    status = db.Column(db.String(20), default="貸出可能")

# データベースの初期化
with app.app_context():
    db.create_all()

# --- ルーティング ---

@app.route('/')
def index():
    # Render（プロキシ）環境でアクセス元の本当のIPアドレスを取得
    # X-Forwarded-For ヘッダーから取得（なければ remote_addr）
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        user_ip = request.remote_addr
    
    # Renderのダッシュボード「Logs」に表示されます
    print(f"アクセスがありました！相手のIPアドレス: {user_ip}")
    
    books = Book.query.all()
    return render_template('index.html', books=books)

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
            # 著者リストをカンマ区切りの文字列に変換
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
    book = db.session.get(Book, book_id) # SQLAlchemy 2.0 推奨の書き方
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
    # ローカル実行用設定
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))