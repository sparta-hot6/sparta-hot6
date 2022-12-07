from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_args
import pymysql
import dbfunction

app = Flask(__name__)

app.template_folder = "templates"


# generating data for pagination - 페이지 매김을 위한 데이터 생성
# users 부분을 mysql과 연동하면 될 듯
posts = dbfunction.get_posts_all()
print(posts)
def get_posts(offset, per_page):
    return posts[offset:offset + per_page]


@app.route('/')
def index():
    #page 현재 페이지 번호, per_page 페이지당 보여줄 게시물 개수
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

if __name__ == "__main__":
    app.run(debug=True)
