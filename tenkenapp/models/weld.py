from tenkenapp import db

class Weld1(db.Model):
    __tablename__ = 'weld-weld_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class Weld_Robot(db.Model):
    __tablename__ = 'weld-robot_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class Fiver_Hand(db.Model):
    __tablename__ = 'weld-fiverhand_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容

class AlufaJULIA(db.Model):
    __tablename__ = 'weld-alufajulia_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(50),nullable=False)  # 点検リスト
    contents = db.Column(db.String(50),nullable=False) #点検内容