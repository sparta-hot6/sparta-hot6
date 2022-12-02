from flask import Flask, render_template
import pymysql


app = Flask(__name__)


# 패스워드는 각자 다를 것이니 수정해서 사용할 것. (passwd='자기비밀번호')
# 라우트 내부에서 db = connect_db() 형식으로 이용.
def connect_db():
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='sparta', db='hotsix', charset='utf8')
    return db


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
