from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

#蓝图
from book import bookbp
from book2 import bookbp2
app.register_blueprint(bookbp,url_prefix="/book")
app.register_blueprint(bookbp2,url_prefix="/book2")


@app.route('/',methods=["GET","POST"])
def index():
    #GET获取 http://127.0.0.1:5000/?page=1&pagenum=20
    if request.method == "GET":
        print(request.args.get("page"))
        print(request.args.get("pagenum"))
    #POST获取
    if request.method == "POST":
        if request.is_json:
            print(request.json.get("username"))  #json格式
        else:
            print(request.form.get("username"))  #form格式
        return "post"


    return render_template("index.html")

@app.route('/keke2')
def keke():
    return "hello keke"

if __name__=="__main__":
    app.run(debug=True)