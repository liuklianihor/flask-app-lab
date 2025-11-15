from flask import Flask, render_template, request, url_for, redirect, Blueprint # type: ignore

post_bp = Blueprint('users', __name__, template_folder='templates')

@post_bp.route("/h1/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/h1.html", name=name, age=age)

@post_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)
