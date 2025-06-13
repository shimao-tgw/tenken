from tenkenapp import db

class Digital_nogisu(db.Model):
    __tablename__ = 'kensa-digital_nogisu_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Analog_nogisu(db.Model):
    __tablename__ = 'kensa-analog_nogisu_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Keyence(db.Model):
    __tablename__ = 'kensa-keyence_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容