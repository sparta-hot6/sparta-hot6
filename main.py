from flask import url_for, session, Flask, render_template , request , redirect, flash
import requests
import pymysql
import logging
import logging.handlers
from api import api

from loginfunctions import confirm_name_id_pw
import string
import dbfunction # db를 다루는 함수를 만들어서 가져다 씁시다. dbfunction.함수() 형식으로 가져올수있습니다.

app = Flask(__name__)
app.secret_key = "hotsix_secret_key"

# 로그 생성
logger = logging.getLogger('hotsix')
# 로그의 출력 기준 설정
logger.setLevel(logging.DEBUG)
# log 출력 형식
formatter = logging.Formatter(
    '[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
# handler 생성
streamHandler = logging.StreamHandler()
log_max_size = 10 * 1024 * 1024
log_file_count = 20
fileHandler = logging.handlers.RotatingFileHandler(filename='./log.txt', maxBytes=log_max_size,
                                                   backupCount=log_file_count)
# logger instance에 fomatter 설정
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# logger instance에 handler 설정
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

# ---- home -- 뉴스 피드 구역 ---------------------------------------------------------------
@app.route('/')
def home():
    # PRIMARY_KEY_ID = 로그인한 유저의 고유번호 입니다.
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html", user_name=session.get("login_name"), login=True)
    else:
        return render_template("index.html", login=False)


# ---- login -- 로그인 구역 -----------------------------------------------------------------
@app.route('/login', methods = ["GET","POST"])
def login():
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html", user_name = session.get("login_name"), login = True)

    login_confirm = ''
    if request.method == 'POST':
        # login 화면에서 input받은 값을 가져옵니다.
        input_id = request.form['floatingInput']
        # login 화면에서 input받은 값을 가져옵니다.
        input_pw = request.form['floatingPassword']
        print(input_id, input_pw)
        # input값들이 db에 있는지 체크 없다면 None 입니다.
        login_info = dbfunction.get_user_table(input_id, input_pw)

        # None이 아닐경우 session 저장됩니다.
        if login_info is not None:
            # session 으로 name 을 저장해 유저의 이름을 활용할수있습니다.
            session['login_name'] = login_info["name"]
            # session 으로 유저의 고유번호를 저장
            session['PRIMARY_KEY_ID'] = login_info["id"]
            # 세션이 저장되고 home 으로 보냅니다.
            return redirect(url_for("home"))

        elif login_info is None:
            # input값들과 같은것이 없다면 에러 (None일 경우)
            login_confirm = 'Please check your ID or password'
            return render_template('login.html', login_confirm=login_confirm)

    # POST 요청이 오기전에는 login.html을 렌더링 해줍니다.
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("PRIMARY_KEY_ID")                                  # 로그아웃 버튼을 누르면 세션이 제거됩니다.
    return redirect(url_for("home"))                               

# ---- signup -- 회원가입  ------------------------------------------------------------------
@app.route("/signup", methods = ["GET","POST"])                               
def signup():
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html", user_name = session.get("login_name"), login = True)

    already_name_msg = ''
    already_id_msg   = ''
    if request.method == 'POST':                                                      # POST 요청이 왔을때만 if문이 실행됩니다.
        input_name = request.form["signup_input_name"]                
        input_id   = request.form["signup_input_id"]
        input_pw   = request.form["signup_input_pw"]
        
        confirm_name = confirm_name_id_pw.confirm_name(input_name)
        confirm_id   = confirm_name_id_pw.confirm_id(input_id)
        confirm_pw   = confirm_name_id_pw.confirm_pw(input_pw) 

        already_exists_name = dbfunction.already_exists_id_name(input_name, 'name')   # 이미 회원가입이 되어있는 아이디인지 체크합니다.
        already_exists_id   = dbfunction.already_exists_id_name(input_id, 'login_id')

        if already_exists_name != None:
            already_name_msg = f'{input_name}은 이미 가입된 이름입니다 이름, 혹은 닉네임으로 입력해주세요.'
            return render_template('signup.html' , already_name_msg = already_name_msg) # ID가 이미 가입된 아이디일 경우 DB에 저장되지않고 다시 회원가입 페이지로 갑니다.
        
        if already_exists_id != None:
            already_id_msg   = f'{input_id}은 이미 가입된 ID 입니다.'
            return render_template('signup.html' , already_id_msg = already_id_msg)

        if confirm_id is not True:
            return render_template('signup.html', confirm_id_msg = confirm_id)      # 3가지 모두 True가 아니면 넘어가지 않습니다.
        if confirm_name is not True:
            return render_template('signup.html', confirm_name_msg = confirm_name)  # 길이, 문자, 숫자 를 검사하고 맞으면 True , 통과하지못하면 메세지를 반환합니다.
        if confirm_pw is not True:
            return render_template('signup.html', confirm_pw_msg = confirm_pw)    


        if already_exists_name == None and already_exists_id == None:
            dbfunction.save_user_info(input_name, input_id, input_pw)               # MySQL 데이터베이스에 새로운 사용자를 추가 하고 회원가입 메시지를 반환합니다.
            return redirect(url_for("signupsucceded"))                              # 회원가입 성공 페이지로 이동합니다.

    return render_template('signup.html')                                           # POST요청 없을떄는 render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/profileupdate')
def profile_update():
    return render_template('profile_update.html')



@app.route("/signupsucceded")                       # 회원가입 완료
def signupsucceded():
    return render_template("signupsucceded.html")

@app.route("/withdrawal")                           # 회원탈퇴
def withdrawal():
    pass


# ---- login -- 로그인 구역 ----------------------------------------------------------------


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
