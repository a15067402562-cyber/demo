from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

class Config(object):
    debug = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flask_study?charset=utf8"

app.config.from_object(Config)

db=SQLAlchemy(app=app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

@app.route('/')
def index():
    # #增加
    # stu1=Student(name="xiaoming")
    # stu2=Student(name="xiaohong")
    # db.session.add(stu1)
    # db.session.add(stu2)
    # db.session.commit()

    # #删除
    # Student.query.filter(Student.id==2).delete()
    # db.session.commit()

    # #修改
    # Student.query.filter(Student.id==1).update({"name":"zhangsan"})
    # db.session.commit()

    #查看
    print(Student.query.get(1).name)
    print(Student.query.all())

    return 'test'

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)