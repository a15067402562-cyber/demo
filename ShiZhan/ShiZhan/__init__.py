from flask import Flask, request, session, redirect


def auth():  #拦截器
    if request.path.startswith("/static"):
        return
    if request.path=="/login":
        return
    user_info=session.get("user_info")
    if user_info:
        return

    return redirect("/login")



def get_real_name():
    user_info=session.get("user_info")
    return user_info["real_name"]

def create_app():
    app =Flask(__name__)
    app.secret_key="sdadhflaholahdhoaiaskljhdoasjo"

    from .views import account
    app.register_blueprint(account.ac)
    from .views import order
    app.register_blueprint(order.od)

    app.before_request(auth)
    app.template_global()(get_real_name)
    return app