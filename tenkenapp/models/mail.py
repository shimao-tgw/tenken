from tenkenapp import db

class Email_parameter(db.Model):
    __tablename__ = 'email_parameter_tbl'
    id = db.Column(db.Integer, primary_key=True)
    work_base_date = db.Column(db.Date, nullable=True)
    work_base_time = db.Column(db.Time, nullable=True)
    current_worker = db.Column(db.String, nullable=True)
    send_flag = db.Column(db.Boolean, nullable=True, default=True)

class CompressorMail(db.Model):
    __tablename__ = 'comp-email_tbl'
    id = db.Column(db.Integer, primary_key=True)
    busyo = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)  

    def __init__(self, busyo, name, email):
        self.busyo = busyo
        self.name = name
        self.email = email

class Email_schedule(db.Model):
    __tablename__ = 'comp-email_schedule_tbl'
    id = db.Column(db.Integer, primary_key=True)
    busyo = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    work_start_date = db.Column(db.Date, nullable=True)
    work_end_date = db.Column(db.Date, nullable=True)
    last_mail_send_date = db.Column(db.DateTime, nullable=True)
    biko = db.Column(db.String(50), nullable=True)