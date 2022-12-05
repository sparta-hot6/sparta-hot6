
from flask import url_for, session, Flask, render_template , request , redirect, jsonify, flash
import requests
import pymysql
import logging
from dbclass import Get_db

app = Flask(__name__)
app.secret_key = "hoon"

# 로그 생성
logger = logging.getLogger('test')

# 로그의 출력 기준 설정
logger.setLevel(logging.DEBUG)

# log 출력 형식
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
# handler 생성
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./test.log')
# logger instance에 fomatter 설정
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# logger instance에 handler 설정
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)


# 패스워드는 각자 다를 것이니 수정해서 사용할 것. (passwd='자기비밀번호')
# 라우트 내부에서 db = connect_db() 형식으로 이용.
def connect_db():
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='sparta', db='hotsix', charset='utf8')
    return db


@app.route('/')
def home():
    if "login_id" in session:
        return render_template("index.html", user_name=session.get("login_id"), login=True), logger.info('로그인 성공 메인')
    else:
        return render_template("index.html", login=False), logger.info('로그인 실패 메인')
# ---- hoon -- 로그인 구역
@app.route('/login', methods=["GET", "POST"])
def login():
    login_succed = "login succed"

    input_id = request.args.get("floatingInput")
    input_pw = request.args.get("floatingPassword")

    login_arr = Get_db.login_confirm(input_id, input_pw)
    name = login_arr[0]
    login_confirm = login_arr[1]

    if login_confirm == login_succed:
        session["login_id"] = name
        return redirect(url_for("home")), logger.info('로그인 성공')

    if request.method == "GET":
        if login_confirm != login_succed:
            # flash(login_confirm)
            # return render_template('login.html')
            return render_template('login.html', login_confirm=login_confirm), logger.info('로그인 하세요')

@app.route('/logout')
def logout():
    session.pop("login_id")
    return redirect(url_for("home")), logger.info('로그아웃')

@app.route('/signup')
def sginup():
    return render_template('signup.html'), logger.info('회원가입 페이지')


@app.route('/signupsucceded')
def route():
    pass


# ---- hoon -- 로그인 구역

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
