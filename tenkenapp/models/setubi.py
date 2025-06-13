from tenkenapp import db

class Nct(db.Model):
    __tablename__ = 'nct_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"
    
class Baritori(db.Model):
    __tablename__ = 'baritori_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"
    
class Press(db.Model):
    __tablename__ = 'press_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"
    
class Tap(db.Model):
    __tablename__ = 'tap_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"
    
class Bender(db.Model):
    __tablename__ = 'bender_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"

class Spot(db.Model):
    __tablename__ = 'spot_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"

class Weld(db.Model):
    __tablename__ = 'weld_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    
    def __repr__(self):
        return f"{self.setubi}"

class Kensa(db.Model):
    __tablename__ = 'kensa_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(20),nullable=False)  # 設備リスト
    serial_no = db.Column(db.String(10),nullable=False)  # 管理番号
    kensa_no = db.Column(db.String(10),nullable=False)  # 検査管理番号
    
    def __repr__(self):
        return f"{self.setubi}"

class Syukka(db.Model):
    __tablename__ = 'syukka_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(45))  # 工程名
    
    def __repr__(self):
        return f"{self.setubi}"
    
class Compressor_setubi(db.Model):
    __tablename__ = 'compressor_setubi_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    setubi = db.Column(db.String(45))  # 工程名
    
    def __repr__(self):
        return f"{self.setubi}"