from flask import url_for, session, Flask, render_template , request , redirect
import requests
import pymysql

import dbfunction # db를 다루는 함수를 만들어서 가져다 씁시다. dbfunction.함수() 형식으로 가져올수있습니다.

app = Flask(__name__)
app.secret_key = "hotsix_secret_key"


# ---- home -- 뉴스피드 구역 ---------------------------------------------------------------
@app.route('/')
def home():
    # PRIMARY_KEY_ID = 로그인한 유저의 고유번호 입니다.
    if "PRIMARY_KEY_ID" in session:
        return render_template("index.html", user_name = session.get("login_name"), login = True)
    else:
        return render_template("index.html", login = False)
    

# ---- login -- 로그인 구역 ----------------------------------------------------------------
@app.route('/login', methods = ["GET","POST"])
def login():
    login_confirm = ''
    if request.method == 'POST':
        input_id = request.form['floatingInput']                   # login 화면에서 input받은 값을 가져옵니다.
        input_pw = request.form['floatingPassword']                # login 화면에서 input받은 값을 가져옵니다.
        print(input_id, input_pw)
        login_info = dbfunction.get_user_table(input_id, input_pw) # input값들이 db에 있는지 체크 없다면 None 입니다.
    
        if login_info is not None:                                 # None이 아닐경우 session 저장됩니다.
            session['login_name']      = login_info["name"]        # session 으로 name 을 저장해 유저의 이름을 활용할수있습니다.
            session['PRIMARY_KEY_ID']  = login_info["id"]          # session 으로 유저의 고유번호를 저장 
            return redirect(url_for("home"))                       # 세션이 저장되고 home 으로 보냅니다.

        elif login_info is None:                                                    
            login_confirm = 'Please check your ID or password'     # input값들과 같은것이 없다면 에러 (None일 경우)
            return render_template('login.html', login_confirm = login_confirm)
            
    return render_template('login.html')                           # POST 요청이 오기전에는 login.html을 렌더링 해줍니다.


@app.route('/logout')
def logout():
    session.pop("PRIMARY_KEY_ID")
    return redirect(url_for("home"))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupsucceded')
def route():
    pass
# ---- login -- 로그인 구역 ----------------------------------------------------------------
















if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
