from tenkenapp import db

class Tap1(db.Model):
    __tablename__ = 'tap-tap1_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class Cts1(db.Model):
    __tablename__ = 'tap-cts1_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容
