from tenkenapp import db

class Spotweld(db.Model):
    __tablename__ = 'spot-spotweld_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class Myspot(db.Model):
    __tablename__ = 'spot-myspot_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容
