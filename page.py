from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
app = Flask(__name__)

app.template_folder = "templates"

#index route
#generating data for pagination
users = list(range(100))
def get_users(offset=0,per_page=5):
    return users[offset:offset+per_page]
@app.route('/')
def index():
    page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter="per_page")
    total = len(users)
    pagination_users = get_users(offset=offset,per_page=per_page)
    pagination = Pagination(page=page,per_page=per_page,total=total,css_framework='bootstrap5')
    return render_template('page.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
if __name__=="__main__":
    app.run(debug=True)