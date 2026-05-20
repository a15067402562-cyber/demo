import hashlib
import json
import uuid

import pymysql
import redis
from flask import Flask, jsonify
from flask import request
app=Flask(__name__)
REDIS_CONN_PARAMS={
        "host":"127.0.0.1",
        "port":6379,
        "encoding":"utf-8",
    }
REDIS_POOL=redis.ConnectionPool(**REDIS_CONN_PARAMS) #Redis连接池
TASK_QUEUE="spider_task_list"
RESULT_QUEUE="spider_result_list"

@app.route('/task',methods=["POST"])
def task():
    ordered_string=request.json.get("ordered_string")
    if not ordered_string:
        return jsonify({"status":False,"error":"参数错误"})

    #Redis模拟队列
    tid=str(uuid.uuid4())
    task_dict={"tid":tid,"data":ordered_string}

    conn=redis.Redis(connection_pool=REDIS_POOL)
    conn.lpush(TASK_QUEUE,json.dumps(task_dict))


    return jsonify({"status":True,"data":tid,"message":"正在处理中，预计1分钟完成"})


@app.route("/result",methods=["GET"])
def result():
    tid=request.args.get("tid")
    if not tid:
        return jsonify({"status": False, "error": "参数错误"})

    conn = redis.Redis(**REDIS_CONN_PARAMS)
    sign=conn.hget(RESULT_QUEUE,tid)
    if not sign:
        return jsonify({"status":True,"data":"","message":"未完成，请继续等待"})
    sign_string=sign.decode("utf-8")
    conn.hdel(RESULT_QUEUE,tid)


    return jsonify({"status":True,"data":sign_string})





if __name__=="__main__":
    app.run(debug=True)