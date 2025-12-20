from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの設定：library.db というファイルに保存する
# app.configの[SQLALCHEMY_DATABASE_URI]=はsqliteの--というファイルです。と設定している。内の値を
# sqliteはSQライトで、:///はここから先がファイル名という目印。
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースのモデル（台帳の項目）
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)      # 自動で割り振られる番号
    title = db.Column(db.String(100), nullable=False) # 本のタイトル
    status = db.Column(db.String(20), default="貸出可能") # 貸出状態

# データベースの初期化（初回起動時にファイルを作成）
with app.app_context():
    db.create_all()

# --- ルーティング（ページごとの処理） ---

@app.route('/')
def index():
    # IPアドレスの表示
    user_ip=request.remote_addr
    print(f"アクセスがありました！相手のIPアドレス{user_ip}")
    # 全ての本をデータベースから取得して画面に表示
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    # 新しい本を登録する
    title = request.form.get('book_name')
    if title:
        new_book = Book(title=title)
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    # 本を「貸出中」にする
    book = Book.query.get(book_id)
    if book:
        book.status = "貸出中"
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    # 本を「貸出可能」に戻す
    book = Book.query.get(book_id)
    if book:
        book.status = "貸出可能"
        db.session.commit()
    return redirect(url_for('index'))
# アクセスしてきた人のIPアドレスを調べる


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")