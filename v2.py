import hashlib

from flask import Flask, jsonify
from flask import render_template
from flask import request

app=Flask(__name__)

@app.route('/bili',methods=["POST"])
def bili():
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