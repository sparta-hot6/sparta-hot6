from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_args
import pymysql
from dbclass import Get_db

app = Flask(__name__)

app.template_folder = "templates"


# generating data for pagination - 페이지 매김을 위한 데이터 생성
# users 부분을 mysql과 연동하면 될 듯
def connect_db():
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='gks1004*', db='hotsix', charset='utf8')
    return db


posts = Get_db.get_db_post()


def get_posts(offset=0, per_page=10):
    return posts[offset:offset + per_page]


@app.route('/', methods=('GET',))
def index():
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
    total = len(posts)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_pagee=per_page, total=total, css_framework='bootstrap5')
    return render_template(
        'page.html',
        posts=pagination_posts,
        page=page,
        per_page=per_page,
        pagination=pagination)

    return jsonify(posts)


if __name__ == "__main__":
    app.run(debug=True)
