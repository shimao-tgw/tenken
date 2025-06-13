from tenkenapp import db

class Koutei(db.Model):
    __tablename__ = 'koutei_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    koutei = db.Column(db.String(45))  # 工程名

    def __repr__(self):
        return f"{self.koutei}"

class Person(db.Model):
    __tablename__ = 'person_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    name = db.Column(db.String(20))  # 個人名
    busyo = db.Column(db.String(20)) #部署名
    email = db.Column(db.String(30)) #メールアドレス


class Tenken(db.Model):
    __tablename__ = 'tenken_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    busyo_name = db.Column(db.String(20),nullable=False)  # 部署
    setubi_name = db.Column(db.String(45),nullable=False)  # 設備
    c1 = db.Column(db.String(10),nullable=False)  # 点検項目1 OK or NG
    c2 = db.Column(db.String(10),nullable=False)  # 点検項目2
    c3 = db.Column(db.String(10),nullable=False)  # 点検項目3
    c4 = db.Column(db.String(10),nullable=False)  # 点検項目4
    c5 = db.Column(db.String(10),nullable=False)  # 点検項目5
    c6 = db.Column(db.String(10),nullable=True)  # 点検項目6
    c7 = db.Column(db.String(10),nullable=True)  # 点検項目7
    c8 = db.Column(db.String(10),nullable=True)  # 点検項目8
    c9 = db.Column(db.String(10),nullable=True)  # 点検項目9
    c10 = db.Column(db.String(10),nullable=True)  # 点検項目10
    c11 = db.Column(db.String(10),nullable=True)  # 点検項目11
    c12 = db.Column(db.String(10),nullable=True)  # 点検項目12
    c13 = db.Column(db.String(10),nullable=True)  # 点検項目13
    c14 = db.Column(db.String(10),nullable=True)  # 点検項目14
    c15 = db.Column(db.String(10),nullable=True)  # 点検項目15
    c16 = db.Column(db.String(10),nullable=True)  # 点検項目16
    c17 = db.Column(db.String(10),nullable=True)  # 点検項目17
    c18 = db.Column(db.String(10),nullable=True)  # 点検項目18
    c19 = db.Column(db.String(10),nullable=True)  # 点検項目19
    c20 = db.Column(db.String(10),nullable=True)  # 点検項目20
    c21 = db.Column(db.String(10),nullable=True)  # 点検項目21
    c22 = db.Column(db.String(10),nullable=True)  # 点検項目22
    c23 = db.Column(db.String(10),nullable=True)  # 点検項目23
    c24 = db.Column(db.String(10),nullable=True)  # 点検項目24
    c25 = db.Column(db.String(10),nullable=True)  # 点検項目25
    tenken_date = db.Column(db.DateTime,nullable=False)  # 点検日
    tenken_person = db.Column(db.String(10),nullable=False) #点検者
    gr_check = db.Column(db.String(10),nullable=True) #グリースアップ実施
    grease_date = db.Column(db.DateTime,nullable=True)  # グリスアップ実施日
    grease_person = db.Column(db.String(10)) # グリスアップ作業者
    biko = db.Column(db.String(100)) # 備考
    nc_1st_oil_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーオイル
    nc_2nd_filter_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーフィルター
    nc_4th_cylinder_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーシリンダー
    nc_4th_piston_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーピストン
    nc_4th_pistonring_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーピストンリング
    nc_4th_fethervalve_date = db.Column(db.Date,nullable=True) #NCTコンプレッサーフェザーバルブ
    nc_4th_conrod_date = db.Column(db.Date,nullable=True) #NCTコンプレッサー連接棒
    nc_4th_non_returnvalve_date = db.Column(db.Date,nullable=True) #NCTコンプレッサー逆止め弁中身セット
    nc_1st_oil_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーオイル
    nc_2nd_filter_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーフィルター
    nc_4th_cylinder_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーシリンダー
    nc_4th_piston_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーピストン
    nc_4th_pistonring_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーピストンリング
    nc_4th_fethervalve_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサーフェザーバルブ
    nc_4th_conrod_person = db.Column(db.String(10),nullable=True) #NCTコンプレッサー連接棒
    nc_4th_non_returnvalve_person = db.Column(db.String(10),nullable=True)
    model_no = db.Column(db.String(10),nullable=False)  # 出荷フォークリフト 型式
    product_no = db.Column(db.String(15),nullable=False)  # 出荷フォークリフト製造番号
    hour_meter = db.Column(db.Float,nullable=False)  # アワーメーター
    syuzenkasyo = db.Column(db.String(50),nullable=True)  #　出荷フォークリフト　修繕箇所及び不具合状況
    syuzen_irai_date = db.Column(db.Date,nullable=True) #　出荷フォークリフト　修繕箇依頼日
    syuzen_date = db.Column(db.Date,nullable=True)  # 出荷フォークリフト　修繕年月日
    syuzen_naiyo = db.Column(db.String(50),nullable=True)  #　出荷フォークリフト修繕実施内容
    nct_air_pressure = db.Column(db.Float,nullable=False)  # エアー圧
    nct_residual_pressure = db.Column(db.Float,nullable=False)  # アシストガスの残圧