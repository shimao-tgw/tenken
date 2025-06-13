from tenkenapp import db

class Senjyoki(db.Model):
    __tablename__ = 'syukka-senjyoki_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容
    
class Senjyoki_monthly(db.Model):
    __tablename__ = 'syukka-monthly_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class Forklift_model(db.Model):
    __tablename__ = 'syukka-forklift-model_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    model_no = db.Column(db.String(10),nullable=False)  # 型式
    product_no = db.Column(db.String(15),nullable=False)  # 製造番号
    user =  db.Column(db.String(10),nullable=False)  # 型式

class Forklift(db.Model):
    __tablename__ = 'syukka-forklift_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容
    kensa_method = db.Column(db.String(10),nullable=False) #検査方法