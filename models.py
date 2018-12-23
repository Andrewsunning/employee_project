from exts import db

class Employee(db.Model):
    __tablename__ = "employee"
    EID = db.Column(db.String(20) , primary_key=True )
    Ename = db.Column(db.String(20) , nullable=False)
    password = db.Column(db.String(100) , nullable=False)
    job = db.Column(db.String(20) , nullable=False)
    basicWage = db.Column(db.Integer , nullable=False)

class Wage(db.Model):
    __tablename__ = "wage"
    WID = db.Column(db.Integer , primary_key=True ,autoincrement=True)
    basicWage = db.Column(db.Integer , nullable=False)
    checkWage = db.Column(db.Integer , nullable=False)
    overTimeWage = db.Column(db.Integer , nullable=False)
    realWage = db.Column(db.Integer , nullable=False)
    date = db.Column(db.String(20), nullable=False)
    EID = db.Column(db.String(20) ,db.ForeignKey('employee.EID') )
    employee = db.relationship('Employee' , backref = db.backref('wage'))

class Check(db.Model):
    __tablename__ = "check_table"
    CID = db.Column(db.Integer , primary_key=True , autoincrement=True)
    lateTimes = db.Column(db.String(20) , nullable=False)
    earlyTimes = db.Column(db.String(20) , nullable=False)
    leaveTimes = db.Column(db.String(20) , nullable=False)
    date = db.Column(db.String(20) ,nullable=False)
    EID = db.Column(db.String(20), db.ForeignKey('employee.EID'))
    employee = db.relationship('Employee' , backref = db.backref("check"))

class FeedBack(db.Model):
    __tablename__ = "feedback"
    FID = db.Column(db.Integer , primary_key=True , autoincrement=True)
    feedText = db.Column(db.Text , nullable=True)
    date = db.Column(db.String(20) ,nullable=False)
    EID = db.Column(db.String(20), db.ForeignKey('employee.EID'))
    employee = db.relationship('Employee' , backref = db.backref("feedBack"))