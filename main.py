from flask import Flask, render_template
import pymysql

import logging
logging.basicConfig(
    level=logging.CRITICAL,
    format = '{asctime} {levelname:<8} {message}',
    style= '{',
    filename='%slog'%__file__[:-2],
    filemode = 'w'
)
logging.debug('This is a debug msg')
logging.info('This is a info msg')

# 로거 세팅
# logger = logging.getLogger("postprocessor")
# logger.setLevel(logging.DEBUG)

# # 일반 핸들러, 포매터 세팅
# formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)

# # 크리티컬 이벤트에 대한 핸들러, 포매터 세팅
# formatter_critical = logging.Formatter("!!!!!%(asctime)s %(levelname)s:%(message)s")
# handler_critical = logging.FileHandler("log_event.log")
# handler_critical.setLevel(logging.CRITICAL)
# handler_critical.setFormatter(formatter_critical)

# # 각 핸들러를 로거에 추가
# logger.addHandler(handler)
# logger.addHandler(handler_critical)

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
