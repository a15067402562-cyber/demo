from flask import Blueprint, render_template, request, redirect,session
from utils import db

ac=Blueprint('account',__name__)

@ac.route('/')
def index():
    return redirect('/login')


@ac.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")

    role=request.form.get('role')
    mobile=request.form.get('mobile')
    pwd=request.form.get('pwd')
    print(role, mobile, pwd)

    #连接MYSQL并执行SQL语句查询用户名密码是否正确
    user_dict=db.fetch_one("select * from user_info where role=%s and mobile=%s and password=%s",[role,mobile,pwd])
    print(user_dict)
    if user_dict:
        session["user_info"]={"role":user_dict["role"],"real_name":user_dict["real_name"],"id":user_dict["id"]}


        return redirect("order/list")
    else:
        return render_template("login.html",error="用户名或密码错误")


    return "ok"



@ac.route("/logout")
def logout():
    session.pop("user_info", None)
    return redirect("/login")


@ac.route("/users")
def users():
    return "用户列表"