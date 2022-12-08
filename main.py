from flask import url_for, session, Flask, render_template, request, redirect, flash, abort, make_response, Response
import requests
import pymysql
import logging
from flask_paginate import Pagination, get_page_args
import logging.handlers
from api import api
from pymysql.cursors import DictCursor

from loginfunctions import confirm_name_id_pw
import string
import dbfunction  # db를 다루는 함수를 만들어서 가져다 씁시다. dbfunction.함수() 형식으로 가져올수있습니다.

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = "hotsix_secret_key"

# ---- logging -- 로그 구역 ----------------------------------------------------------------
# 로그 생성
logger = logging.getLogger('hotsix')
info_logger = logging.getLogger('work')
# 로그의 출력 기준 설정
logger.setLevel(logging.DEBUG)
info_logger.setLevel(logging.INFO)
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
info_logger.addHandler(fileHandler)
# --------------- 로그 생성 설정 구역 ------------------------------

# 페이지네이션 관련 함수----------
posts = dbfunction.get_posts_all()


def get_posts(offset=0, per_page=10):
    # 여기서 설정이 변경됨으로 나오는 페이지 관리가 되야하는데 안됨
    return posts[offset: offset + per_page]


# 페이지네이션 관련 함수--------------------


# ---- home -- 뉴스 피드 구역 ---------------------------------------------------------------


@app.route('/')
def home():
    page, per_page, offset = get_page_args(page_parameter="page",
                                           per_page_parameter="per_page")
    total = len(posts)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page,
                            per_pagee=per_page,
                            total=total,
                            css_framework='bootstrap5')
    # PRIMARY_KEY_ID = 로그인한 유저의 고유번호 입니다.
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html",
                               user_name=session.get("login_name"),
                               login=True,
                               posts=pagination_posts,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               ), logger.info('로그인 상태'), info_logger.info('로그인상태')
    else:
        return render_template("index.html",
                               login=False,
                               posts=pagination_posts,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               ), logger.info('로그아웃 상태'), info_logger.info('로그아웃 상태')


# ---- login -- 로그인 구역 -----------------------------------------------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if "PRIMARY_KEY_ID" in session:  # 세션이 있을때는 뒤로가기, 임의로 사이트주소를 입력해도 홈으로 돌아갑니다.
        return render_template("index.html", user_name=session.get("login_name"), login=True), logger.info(
            '이미로그인 됨'), info_logger.info('이미로그인됨')

    login_confirm = ''
    if request.method == 'POST':
        input_id = request.form['floatingInput']  # login 화면에서 input받은 값을 가져옵니다.
        input_pw = request.form['floatingPassword']  # login 화면에서 input받은 값을 가져옵니다.

        login_info = dbfunction.get_user_table(input_id, input_pw)  # input값들이 db에 있는지 체크 없다면 None 입니다.

        if input_id == '' and input_pw == '':
            login_confirm = '아이디와 비밀번호를 입력해주세요.'
            return render_template('login.html', login_confirm=login_confirm, input_id=input_id), logger.info(
                '로그인 실패'), info_logger.info(
                '로그인 실패')

        elif input_id == '':
            login_confirm = '아이디를 입력해주세요.'
            return render_template('login.html', login_confirm=login_confirm, input_id=input_id), logger.info(
                '로그인 실패'), info_logger.info(
                '로그인 실패')

        elif input_pw == '':
            login_confirm = '비밀번호를 입력해주세요.'
            return render_template('login.html', login_confirm=login_confirm, input_id=input_id), logger.info(
                '로그인 실패'), info_logger.info(
                '로그인 실패')

        elif login_info is None:
            login_confirm = '아이디와 비밀번호를 확인해주세요.'  # input값들과 같은것이 없다면 에러 (None일 경우)
            return render_template('login.html', login_confirm=login_confirm, input_id=input_id), logger.info(
                '로그인 실패'), info_logger.info(
                '로그인 실패')

        elif login_info is not None:  # None이 아닐경우 session 저장됩니다.
            session['login_name'] = login_info["name"]  # session 으로 name 을 저장해 유저의 이름을 활용할수있습니다.
            session['PRIMARY_KEY_ID'] = login_info["id"]  # session 으로 유저의 고유번호를 저장
            return redirect(url_for("home")), logger.info('로그인 성공'), info_logger.info(
                '로그인 성공')  # 세션이 저장되고 home 으로 보냅니다.

    return render_template('login.html')  # POST 요청이 오기전에는 login.html을 렌더링 해줍니다.


@app.route('/logout')
def logout():
    session.clear()  # 로그아웃 버튼을 누르면 모든 세션이 제거됩니다.
    return redirect(url_for("home")), logger.info('로그아웃'), info_logger.info('로그아웃')


# ---- signup -- 회원가입  ------------------------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "PRIMARY_KEY_ID" in session:  # 세션이 있을때는 뒤로가기, 임의로 사이트주소를 입력해도 홈으로 돌아갑니다.
        return render_template("index.html", user_name=session.get("login_name"), login=True), logger.info(
            '로그인 상태'), info_logger.info('로그인 상태')
    # ----------------------------------------------------------------------  -------------------
    already_name_msg = ''
    already_id_msg = ''
    if request.method == 'POST':  # POST 요청이 왔을때만 if문이 실행됩니다.
        input_name = request.form["signup_input_name"]
        input_id = request.form["signup_input_id"]
        input_pw = request.form["signup_input_pw"]

        confirm_name = confirm_name_id_pw.confirm_name(input_name)
        confirm_id = confirm_name_id_pw.confirm_id(input_id)
        confirm_pw = confirm_name_id_pw.confirm_pw(input_pw)

        if input_id == "" and input_name == "" and input_pw == "":  # 입력값이 공백일 경우 input_name = input_name을 붙이는 이유는 새로고침시 입력값을 유지 하기 위함
            return render_template('signup.html', confirm_id_name_pw="이름, 아이디, 비밀번호를 입력해주세요")
        elif input_id == "":
            return render_template('signup.html', confirm_id_msg="아이디를 입력해주세요", input_name=input_name)
        elif input_name == "":
            return render_template('signup.html', confirm_name_msg="이름을 입력해주세요", input_id=input_id)
        elif input_pw == "":
            return render_template('signup.html', confirm_pw_msg="비밀번호를 입력해주세요", input_name=input_name,
                                   input_id=input_id)
        # ----------------------------------------------------------------------
        already_exists_name = dbfunction.already_exists_id_name(input_name, 'name')  # 이미 회원가입이 되어있는 아이디인지 체크합니다.
        already_exists_id = dbfunction.already_exists_id_name(input_id, 'login_id')

        if already_exists_name != None:  # ID가 이미 가입된 아이디일 경우 DB에 저장되지않고 다시 회원가입 페이지로 갑니다.
            already_name_msg = f'{input_name}은 이미 가입된 이름입니다 다른 이름, 혹은 닉네임으로 입력해주세요.'
            return render_template('signup.html', already_name_msg=already_name_msg, input_name=input_name,
                                   input_id=input_id), logger.info(
                '이미있는 이름'), info_logger.info('이미있는 이름')  # ID가 이미 가입된 아이디일 경우 DB에 저장되지않고 다시 회원가입 페이지로 갑니다.

        elif already_exists_id != None:
            already_id_msg = f'{input_id}은 이미 가입된 ID 입니다.'
            return render_template('signup.html', already_id_msg=already_id_msg, input_name=input_name,
                                   input_id=input_id), logger.info(
                '이미있는 ID'), info_logger.info('이미있는 ID')
        # ----------------------------------------------------------------------

        if confirm_id is not True:  # 3가지 모두 True가 아니면 넘어가지 않습니다.
            return render_template('signup.html', confirm_id_msg=confirm_id, input_name=input_name, input_id=input_id)
        if confirm_name is not True:
            return render_template('signup.html', confirm_name_msg=confirm_name, input_name=input_name,
                                   input_id=input_id)
        if confirm_pw is not True:
            return render_template('signup.html', confirm_pw_msg=confirm_pw, input_name=input_name, input_id=input_id)
        # ----------------------------------------------------------------------

        if already_exists_name == None and already_exists_id == None:  # 위의 유효성 검사를 통과한 입력값이 있을시 통과
            dbfunction.save_user_info(input_name, input_id, input_pw)  # MySQL 데이터베이스에 새로운 사용자를 추가 하고 회원가입 메시지를 반환합니다.
            return redirect(url_for("signupsucceded")), logger.info('회원가입 성공'), info_logger.info(
                '회원가입 성공')  # 회원가입 성공 페이지로 이동합니다.

    return render_template('signup.html') , logger.info('회원가입 페이지 이동'), info_logger.info(
        '회원가입 페이지 이동')  # POST요청 없을떄는 render_template('signup.html')


@app.route("/profile", methods=['GET'])
def profile():
    if "PRIMARY_KEY_ID" not in session:
        return redirect(url_for('home'))
    id = session['PRIMARY_KEY_ID']
    curs = dbfunction.MySQL_connect().cursor(DictCursor)
    sql = f"select * from post where id={id}"
    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)
    return render_template("profile.html", login=True, data=rows)


@app.route('/profileupdate')
def profile_update():
    if "PRIMARY_KEY_ID" not in session:
        return redirect(url_for('home'))
    return render_template('profile_update.html', login=True)


@app.route("/signupsucceded")  # 회원가입 완료
def signupsucceded():
    return render_template("signupsucceded.html"), logger.info('가입 완료 페이지'), info_logger.info('가입 완료 페이지')


@app.route("/withdrawal")  # 회원탈퇴 는 구현할 시간이 없네요.
def withdrawal():
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html", user_name=session.get("login_name"), login=True)


# ---- login -- 로그인 구역 ----------------------------------------------------------------


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
