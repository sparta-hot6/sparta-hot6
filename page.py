from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_args, get_page_parameter
import pymysql
import dbfunction

app = Flask(__name__)

posts = dbfunction.get_posts_all()


def get_posts(page,offset=0, per_page=5):
    offset =((page-1)*per_page)
    return posts[offset : offset+per_page]


@app.route('/', methods=('GET',))
def index():

    page, per_page, offset = get_page_args(page_parameter="page",
                                           per_page_parameter="per_page")
    total = len(posts)
    print(page,per_page,offset,total)

    pagination_posts = get_posts(page=page,offset=offset, per_page=per_page)
    print(pagination_posts)
    pagination = Pagination(page=page,
                            per_pagee=per_page,
                            total=total,
                            css_framework='bulma')
    return render_template(
        'hot6.html',
        posts=pagination_posts,
        page=page,
        per_page=per_page,
        pagination=pagination,)


if __name__ == "__main__":
    app.run(debug=True)
