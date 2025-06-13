# tenkenapp/__init__.py
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy  # 追加
from flask_mail import Mail # 追加
from flask_cors import CORS


# Flask拡張のインスタンスを作成（アプリにはまだバインドしない）
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('tenkenapp.config')

    # 拡張機能をアプリに紐付ける
    db.init_app(app)
    mail.init_app(app)
    CORS(app)

    # ここでappコンテキストを作ってviewsをimport（循環参照回避）
    with app.app_context():
        import tenkenapp.views

    return app

