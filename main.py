from flask import url_for, session, Flask, render_template , request , redirect, jsonify, flash
import requests
import pymysql

from dbclass import Get_db

app = Flask(__name__)
app.secret_key = "hoon"

# 패스워드는 각자 다를 것이니 수정해서 사용할 것. (passwd='자기비밀번호')
# 라우트 내부에서 db = connect_db() 형식으로 이용.
def connect_db():
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='930523', db='hotsix', charset='utf8')
    return db

@app.route('/')
def home():
    if "login_id" in session:
        return render_template("index.html", user_name = session.get("login_id"), login = True)
    else:
        return render_template("index.html", login = False)
    
# ---- hoon -- 로그인 구역
@app.route('/login', methods = ["GET","POST"])
def login():
    login_succed = "login succed"

    input_id = request.args.get("floatingInput")
    input_pw = request.args.get("floatingPassword")

    login_arr = Get_db.login_confirm(input_id, input_pw)
    name          = login_arr[0]
    login_confirm = login_arr[1]

    if login_confirm == login_succed:
        session["login_id"] = name
        return redirect(url_for("home"))

    if request.method == "GET":
        if login_confirm != login_succed:
            # flash(login_confirm)
            # return render_template('login.html')
            return render_template('login.html', login_confirm = login_confirm)

@app.route('/logout')
def logout():
    session.pop("login_id")
    return redirect(url_for("home"))

@app.route('/signup')
def sginup():
    return render_template('signup.html')

@app.route('/signupsucceded')
def route():
    pass

# ---- hoon -- 로그인 구역

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
