from tenkenapp import db

class Rg(db.Model):
    __tablename__ = 'bender-rg_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Hds(db.Model):
    __tablename__ = 'bender-hds_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Hg(db.Model):
    __tablename__ = 'bender-hg_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Atc(db.Model):
    __tablename__ = 'bender-atc_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Astro(db.Model):
    __tablename__ = 'bender-astro_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Egb(db.Model):
    __tablename__ = 'bender-egb_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容

class Egar(db.Model):
    __tablename__ = 'bender-egar_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容