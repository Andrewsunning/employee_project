from flask_script import  Manager
from employee_project import app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from models import Employee , Wage , Check , FeedBack
##还要导入models.py中创建的模型

manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app ,db)

#添加迁移脚本的命令到manager
manager.add_command('db' , MigrateCommand)

if __name__ == "__main__":
    manager.run()
