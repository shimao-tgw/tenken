from tenkenapp import db

#テスト用
class Comp_test_list(db.Model):
   __tablename__ = 'compressor-test-tenkenlist_tbl'
   id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
   tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
   contents = db.Column(db.String(20),nullable=False) #点検内容

class Comp_list(db.Model):
    __tablename__ = 'compressor-tenkenlist_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    tenken_list = db.Column(db.String(20),nullable=False)  # 点検リスト
    contents = db.Column(db.String(20),nullable=False) #点検内容
    input_type = db.Column(db.String(15),nullable=False) #テキストボックスかチェックボックスか、ラジオボタンか
    select_text = db.Column(db.String(10),nullable=False) #選択項目
    unit_text = db.Column(db.String(10),nullable=False) #単位
    name = db.Column(db.String(30),nullable=False) #保存用name

class Comp_tenken(db.Model):
    __tablename__ = 'compressor-tenken_tbl'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    inspection_id = db.Column(db.String(15), unique=True, nullable=False) #作業ごとのID
    setubi_name = db.Column(db.String(15), unique=True, nullable=False) #設備名
    machine_no = db.Column(db.String(10),nullable=False) #何号機か
    c1 = db.Column(db.Integer, nullable=False)  # 稼働時間
    c2 = db.Column(db.Float, nullable=False) #吐出時間
    c3 = db.Column(db.Float, nullable=False) #吐出温度
    c4 = db.Column(db.String(10),nullable=False) #モニター
    c5 = db.Column(db.String(10),nullable=False) #表示ランプ
    c6 = db.Column(db.String(10),nullable=False) #表示ランプ
    c7 = db.Column(db.String(10),nullable=False) #表示ランプ
    c8 = db.Column(db.String(10),nullable=False) #オイル
    c9 = db.Column(db.String(10),nullable=False) #オイル
    c10 = db.Column(db.String(10),nullable=False) #オイル漏れ
    c11 = db.Column(db.String(10),nullable=False) #オイル漏れ
    c12 = db.Column(db.String(10),nullable=False) #振動・異音
    c13 = db.Column(db.String(10),nullable=False) #ダストフィルター清掃
    c14 = db.Column(db.String(10),nullable=False) #ダストフィルター清掃
    c15 = db.Column(db.String(10),nullable=False) #吸込フィルター清掃
    c16 = db.Column(db.String(10),nullable=False) #吸込フィルター交換
    c17 = db.Column(db.String(10),nullable=False) #オイルフィルター交換
    c18 = db.Column(db.String(10),nullable=False) #オイル交換
    c19 = db.Column(db.String(10),nullable=False) #エレメント交換
    c20 = db.Column(db.String(10),nullable=False) #クーラ交換
    c21 = db.Column(db.String(10),nullable=False) #年次点検
    c22 = db.Column(db.String(10),nullable=False) #ドレン漏れ
    c23 = db.Column(db.String(10),nullable=False) #ドレン漏れ
    c24 = db.Column(db.String(10),nullable=False) #水漏れ
    c25 = db.Column(db.String(10),nullable=False) #処理水の汚れ
    c26 = db.Column(db.String(10),nullable=False) #処理水の汚れ
    main_work = db.Column(db.String(10),nullable=False) #メイン稼働号機
    tenken_date = db.Column(db.DateTime,nullable=False)  # 点検日
    tenken_busyo = db.Column(db.String(10),nullable=False) #点検部署
    tenken_person = db.Column(db.String(10),nullable=False) #点検者
    biko = db.Column(db.String(100)) # 備考
    is_completed = db.Column(db.Boolean, default=False, nullable=False) #点検完了済みか