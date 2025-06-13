from tenkenapp import db

class Cdstud(db.Model):
    __tablename__ = 'press-cdstud_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容
    
class Gunman(db.Model):
    __tablename__ = 'press-gunman_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Highspin(db.Model):
    __tablename__ = 'press-highspin1_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Heager(db.Model):
    __tablename__ = 'press-heager_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Press25t45t(db.Model):
    __tablename__ = 'press-press25t_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Shirring(db.Model):
    __tablename__ = 'press-shirring_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class T_driver(db.Model):
    __tablename__ = 'press-tdriver_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    msize = db.Column(db.String(10),nullable=False)  # Mサイズ
    tenken_list = db.Column(db.String(20),nullable=False)  # 設定値
    contents = db.Column(db.String(20),nullable=False) #点検許容値
    driver_no = db.Column(db.String(15),nullable=False) #ドライバー型番
    control_no = db.Column(db.String(15),nullable=False) #管理番号

#まだ使う
class T_driver_tenken(db.Model): #M3,M4兼用
    __tablename__ = 'press-tdriver-check_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    msize = db.Column(db.String(10),nullable=False)  # Mサイズ
    memori = db.Column(db.Float,nullable=False)  # 目盛り位置
    jissoku = db.Column(db.Float,nullable=False) # 実測値
    tenken_date = db.Column(db.DateTime,nullable=False)  # 点検日
    tenken_person = db.Column(db.String(10),nullable=False) #点検者
    biko = db.Column(db.String(45)) # 備考

class Arcstud(db.Model):
    __tablename__ = 'press-arcstud_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容
