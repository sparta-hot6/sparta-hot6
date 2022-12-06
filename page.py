from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_args
import pymysql
import dbfunction

app = Flask(__name__)

posts = dbfunction.get_posts_all()


def get_posts(offset=0, per_page=5):
    # 여기서 설정이 변경됨으로 나오는 페이지 관리가 되야하는데 안됨
    return posts[offset : offset+per_page]


@app.route('/', methods=('GET',))
def index():
    page, per_page, offset = get_page_args(page_parameter="page",
                                           per_page_parameter="per_page")
    total = len(posts)
    pagination_posts = get_posts(offset=offset, per_page=per_page)
    pagination = Pagination(page=page,
                            per_pagee=per_page,
                            total=total,
                            css_framework='bootstrap5')
    return render_template(
        'page.html',
        posts=pagination_posts,
        page=page,
        per_page=per_page,
        pagination=pagination,)


if __name__ == "__main__":
    app.run(debug=True)
