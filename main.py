from flask import url_for, session, Flask, render_template , request , redirect
import pymysql


app = Flask(__name__)
app.secret_key = "hoon"

# 패스워드는 각자 다를 것이니 수정해서 사용할 것. (passwd='자기비밀번호')
# 라우트 내부에서 db = connect_db() 형식으로 이용.
def connect_db():
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='sparta', db='hotsix', charset='utf8')
    return db

@app.route('/')
def home():
    if "login_id" in session:
        return render_template("index.html", user_name = session.get("login_id"), login = True)
    else:
        return render_template("index.html", login = False)
    
# ---- hoon -- 로그인 구역
# db 에서 받은 정보 예시
login_id = "jmoon581"
password = "930523"
name = "정성훈"

@app.route('/login', methods = ["get"])
def login():
    global login_id, password, name
    _id_ = request.args.get("floatingInput")
    _pw_ = request.args.get("floatingPassword")

    if login_id == _id_ and password == _pw_:
        session["login_id"] = name
        return redirect(url_for("home"))
    else:
        return render_template('login.html')

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
