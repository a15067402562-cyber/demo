import hashlib
import pymysql
from flask import Flask, jsonify
from flask import request
from dbutils.pooled_db import PooledDB
app=Flask(__name__)

#创建线程池
POOL=PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[],
    ping=0,
    host="127.0.0.1", port=3306, user="root", passwd="root", charset="utf8", db="flask_study"
)



def fetch_one(sql,params):
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

@app.route('/bili',methods=["POST"])
def bili():
    token=request.json.get("token")
    if not token: #无token
        return jsonify({"status":False,"error":"认证失败"})

    result=fetch_one("select * from user where token=%s",[token,])
    if not result:
        return jsonify({"status":False,"error":"认证失败"})


    ordered_string=request.json.get("ordered_string")
    if not ordered_string:
        return jsonify({"status":False,"error":"参数错误"})

    encrypt_string=ordered_string+"74d89af48b654c8864d997da"
    obj=hashlib.md5(encrypt_string.encode("utf-8"))
    sign=obj.hexdigest()
    return jsonify({"status":True,"data":sign})

@app.route('/keke2')
def keke2():
    return "hello keke2"

if __name__=="__main__":
    app.run(debug=True)