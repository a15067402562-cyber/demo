from flask import Blueprint, session, redirect, render_template,request
from utils import db,cache

od=Blueprint('order',__name__)

@od.route("/order/list")
def order_list():
    user_info=session.get("user_info")
    role=user_info["role"]
    if role==2:
        data_list=db.fetch_all("select * from `order` left join user_info on `order`.user_id=user_info.id",[])
    else:
        data_list=db.fetch_all("select * from `order` left join user_info on `order`.user_id=user_info.id where user_id=%s",[user_info["id"],])

    status_dict={
        1:{"text":"待执行","cls":"primary"},
        2:{"text":"正在执行","cls":"info"},
        3:{"text":"完成","cls":"success"},
        4:{"text":"失败","cls":"danger"},
    }
    print(data_list)

    return render_template("order_list.html",data_list=data_list,status_dict=status_dict,real_name=user_info["real_name"])

@od.route("/order/create",methods=["GET","POST"])
def create_list():

    if request.method=="GET":
        return render_template("order_create.html")
    url=request.form.get("url")
    count=request.form.get("count")

    #写入数据库
    user_info = session.get("user_info")
    params=[url,count,user_info["id"]]
    order_id=db.insert("insert into `order`(url,count,user_id,status) values (%s,%s,%s,1)",params)
    print(order_id)

    #写入redis队列
    cache.push_queue(order_id)
    return redirect("/order/list")

@od.route("/order/delete", methods=["GET", "POST"])
def delete_list():
    if request.method=="GET":
        return render_template("order_delete.html")
    id=request.form.get("id")
    db.delete("delete from `order` where id=%s", [id])
    return redirect("/order/list")