from flask import Flask,render_template,request,redirect , url_for,session
import config
from models import Employee,Wage,Check,FeedBack
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login_putong/' , methods = ['GET' , 'POST'])
def login_putong():
    if request.method == 'GET':
        return render_template("login_putong.html")
    else:
        EID = request.form.get('EID')
        password = request.form.get('password')
        #查询返回一个employee实例
        employee = Employee.query.filter(Employee.EID == EID , Employee.password == password).first()
        if employee:
            session['EID'] = employee.EID
            session.permanent = True

            job = employee.job

            wage = Wage.query.filter(Wage.EID == employee.EID).first()
            basicWage = employee.basicWage
            checkWage = wage.checkWage
            overTimeWage = wage.overTimeWage
            realWage = wage.realWage
            date = wage.date

            check = Check.query.filter(Check.EID == employee.EID).first()
            lateTimes = check.lateTimes
            earlyTimes = check.earlyTimes
            leaveTimes = check.leaveTimes
            context = {
                'job' : job,
                'basicWage' : basicWage,
                'checkWage' : checkWage,
                'overTimeWage' : overTimeWage,
                'realWage' : realWage,
                'date' : date,
                'lateTimes' : lateTimes,
                'earlyTimes' : earlyTimes,
                'leaveTimes' : leaveTimes,
            }

            # 这么引用为什么不行？？？
            # print(employee.wage.checkWage)
            return  render_template('login_putong_operate.html' , **context)
        else:
            return "账号或密码错误，请核对后重输！"



@app.route('/login_hr' , methods = ['GET' , 'POST'])
def login_hr():
    if request.method == 'GET':
        return render_template("login_hr.html")
    else:
        EID = request.form.get('EID')
        password = request.form.get('password')
        # 查询返回一个employee实例
        employee = Employee.query.filter(Employee.EID == EID, Employee.password == password).first()
        if employee:
            session['EID'] = employee.EID
            session.permanent = True
            return render_template('login_hr_operate.html')
        else:
            return "账号或密码错误，请核对后重输！"

@app.route('/login_manager' , methods = ['GET' , 'POST'])
def login_manager():
    if request.method == 'GET':
        return render_template('login_manager.html')
    else:
        EID = request.form.get('EID')
        password = request.form.get('password')
        # 查询返回一个employee实例
        employee = Employee.query.filter(Employee.EID == EID, Employee.password == password).first()
        if employee:
            session['EID'] = employee.EID
            session.permanent = True
            return render_template('login_manager_operate.html')
        else:
            return "账号或密码错误，请核对后重输！"

#普通员工登陆后的操作函数
@app.route('/login_putong/operate/' , methods = ['GET' , 'POST'])
def login_putong_operate():
    EID = session.get('EID')
    # print(EID)
    feedText = request.form.get('content')
    date = request.form.get('month')
    #实例化一个FeedBack类的对象
    feedBack = FeedBack(feedText = feedText , date = date , EID = EID)
    db.session.add(feedBack)
    db.session.commit()
    return "反馈已收到，我们会尽快核实！"

#hr登陆后的操作函数
@app.route('/login_hr/operate/')
def login_hr_operate():
    return "这是hr操作视图函数"

#hr查询员工信息的视图函数
@app.route('/hr_search/' , methods=['GET' , 'POST'])
def hr_search():
    if request.method == "GET":
        return render_template('hr_search.html')
    else:
        EID = request.form.get('EID')
        employee = Employee.query.filter(Employee.EID == EID).first()
        if employee:
            job = employee.job

            wage = Wage.query.filter(Wage.EID == employee.EID).first()
            basicWage = employee.basicWage
            checkWage = wage.checkWage
            overTimeWage = wage.overTimeWage
            realWage = wage.realWage
            date = wage.date

            check = Check.query.filter(Check.EID == employee.EID).first()
            lateTimes = check.lateTimes
            earlyTimes = check.earlyTimes
            leaveTimes = check.leaveTimes
            context = {
                'job': job,
                'basicWage': basicWage,
                'checkWage': checkWage,
                'overTimeWage': overTimeWage,
                'realWage': realWage,
                'date': date,
                'lateTimes': lateTimes,
                'earlyTimes': earlyTimes,
                'leaveTimes': leaveTimes,
            }
            return render_template('hr_search.html' , **context)
        else:
            return "输入有误，请确认后重新输入！"

#hr录入员工信息的视图函数
@app.route('/hr_insert' , methods=['GET' , 'POST'])
def hr_insert():
    if request.method == "GET":
        return render_template('hr_insert.html')
    else:
        EID = request.form.get('EID')
        Ename = request.form.get('Ename')
        password = request.form.get('password')
        job = request.form.get('job')
        date = request.form.get('date')
        lateTimes = request.form.get('lateTimes')
        earlyTimes = request.form.get('earlyTimes')
        leaveTimes = request.form.get('leaveTimes')
        basicWage = int(request.form.get('basicWage'))
        # print(type(basicWage))
        overTimeWage = int(request.form.get('overTimeWage'))
        checkWage = int(request.form.get('checkWage'))
        realWage = basicWage + overTimeWage + checkWage - int(earlyTimes)*10 - int(leaveTimes)*100 - int(lateTimes)*10
        ##该实例化一个新对象了
        employee = Employee(EID = EID , Ename = Ename , password = password , job = job , basicWage = basicWage)
        db.session.add(employee)
        db.session.commit()
        wage = Wage(basicWage = basicWage , checkWage = checkWage , overTimeWage = overTimeWage , realWage = realWage , date = date , EID = EID)
        db.session.add(wage)
        db.session.commit()
        check = Check(lateTimes = lateTimes , earlyTimes = earlyTimes , leaveTimes = leaveTimes ,date = date , EID =EID)
        db.session.add(check)
        db.session.commit()
        return "录入成功"

#hr修改员工工资信息
@app.route('/hr_update/' , methods=['GET' , 'POST'])
def hr_update():
    if request.method == "GET":
        return render_template('hr_update.html')
    else:
        EID = request.form.get('EID')
        Ename = request.form.get('Ename')
        # password = request.form.get('password')
        # job = request.form.get('job')
        date = request.form.get('date')
        lateTimes = request.form.get('lateTimes')
        earlyTimes = request.form.get('earlyTimes')
        leaveTimes = request.form.get('leaveTimes')
        # basicWage = int(request.form.get('basicWage'))
        # print(type(basicWage))
        overTimeWage = int(request.form.get('overTimeWage'))
        checkWage = int(request.form.get('checkWage'))

        employee = Employee.query.filter(Employee.EID == EID).first()
        realWage = employee.basicWage + overTimeWage + checkWage - int(earlyTimes)*10 - int(leaveTimes)*100 - int(lateTimes)*10

        employee.Ename = Ename
        employee.EID = EID
        # employee.job = job
        # employee.basicWage = basicWage
        db.session.commit()
        wage = Wage.query.filter(Wage.EID == EID).first()
        # wage.basicWage = basicWage
        wage.checkWage = checkWage
        wage.overTimeWage = overTimeWage
        wage.realWage = realWage
        wage.date = date
        db.session.commit()
        check = Check.query.filter(Check.EID == EID).first()
        check.lateTimes = lateTimes
        check.earlyTimes = earlyTimes
        check.leaveTimes = leaveTimes
        check.date = date
        db.session.commit()
        return "修改成功！"

@app.route('/hr_search_feedback/' , methods=['GET' , 'POST'])
def hr_search_feedback():
    if request.method == 'GET':
        return render_template('hr_search_feedback.html')
    else:
        date = request.form.get('date')
        feedback = FeedBack.query.filter(FeedBack.date == date).all()
        context = {
            'feedback':feedback,
        }
        return render_template('hr_search_feedback.html' , **context)



#经理登陆后的操作函数
@app.route('/login_manager/operate/')
def login_manager_operate():
    return "这是经理操作视图函数"

@app.route('/manager_search/' , methods=['GET' , 'POST'])
def manager_search():
    if request.method == "GET":
        return render_template('manager_search.html')
    else:
        EID = request.form.get('EID')
        employee = Employee.query.filter(Employee.EID == EID).first()
        if employee:
            job = employee.job

            wage = Wage.query.filter(Wage.EID == employee.EID).first()
            basicWage = employee.basicWage
            checkWage = wage.checkWage
            overTimeWage = wage.overTimeWage
            realWage = wage.realWage
            date = wage.date

            check = Check.query.filter(Check.EID == employee.EID).first()
            lateTimes = check.lateTimes
            earlyTimes = check.earlyTimes
            leaveTimes = check.leaveTimes
            context = {
                'job': job,
                'basicWage': basicWage,
                'checkWage': checkWage,
                'overTimeWage': overTimeWage,
                'realWage': realWage,
                'date': date,
                'lateTimes': lateTimes,
                'earlyTimes': earlyTimes,
                'leaveTimes': leaveTimes,
            }
            return render_template('hr_search.html', **context)
        else:
            return "输入有误，请确认后重新输入！"

@app.route('/manager_update/', methods=['GET' , 'POST'])
def manager_update():
    if request.method == "GET":
        return render_template('manager_update.html')
    else:
        EID = request.form.get('EID')
        Ename = request.form.get('Ename')
        job = request.form.get('job')
        basicWage = request.form.get('basicWage')

        employee = Employee.query.filter(Employee.EID == EID).first()
        employee.Ename = Ename
        employee.job = job
        employee.basicWage = basicWage

        wage = Wage.query.filter(Wage.EID == EID).first()
        wage.basicWage = basicWage
        print(wage.basicWage)
        db.session.commit()
        return "修改成功！"


@app.context_processor
def my_context_processor():
    EID = session.get('EID')
    if EID:
        employee = Employee.query.filter(Employee.EID == EID).first()
        if employee:
            return {"employee":employee}
    return {}

if __name__ == '__main__':
    app.run()
