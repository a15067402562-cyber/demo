import hashlib

from flask import Flask, jsonify
from flask import request

app=Flask(__name__)

#采用本地文件形式获取token
def get_user_dict():
    info_dict={}
    with open("db.txt","r") as f:
        for line in f.readlines():
            line=line.strip()
            token,name=line.split(",")
            info_dict[token]=name
    return info_dict
@app.route('/bili',methods=["POST"])
def bili():
    token=request.json.get("token")
    if not token: #无token
        return jsonify({"status":False,"error":"认证失败"})
    user_dict=get_user_dict()

    if token not in user_dict:  #token不合法
        return jsonify({"status":False,"error":"认证失败"})


    ordered_string=request.json.get("ordered_string")
    if not ordered_string:
        return jsonify({"status":False,"error":"参数错误"})

    encrypt_string=ordered_string+"74d89af48b654c8864d997da"
    obj=hashlib.md5(encrypt_string.encode("utf-8"))
    sign=obj.hexdigest()
    return jsonify({"status":True,"data":sign})

@app.route('/keke2')
def keke():
    return "hello keke"

if __name__=="__main__":
    app.run(debug=True)