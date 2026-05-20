from flask import Blueprint, render_template, session, request, redirect
from utils import db,cache

us=Blueprint("user",__name__)

@us.route("/user/list")
def us_list():
    user_info=session.get("user_info")
    role=user_info.get("role")
    user_list = []
    if role==2:
        user_list=db.fetch_all("select * from `user_info`",[])

    role_dict={
        1:"用户",
        2:"管理员"
    }

    return render_template("user_list.html",user_list=user_list,role_dict=role_dict)

@us.route("/user/create")
def us_create():
    if request.method=="GET":
        return render_template("user_create.html")
    mobile=request.form.get("mobile")
    password=request.form.get("password")
    real_name=request.form.get("real_name")
    role=request.form.get("role")
    print(mobile,password,real_name,role)
    # user_id=db.idu("insert into `user_info`(mobile,password,real_name,role) values (%s,%s,%s,%d)",[mobile,password,real_name,role])
    #
    # cache.push_queue(user_id)
    return redirect("/user/list",)

