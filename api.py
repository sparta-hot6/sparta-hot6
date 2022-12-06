from flask import Blueprint

# api Blueprint를 main에 url_prefix를 /api로 등록시켜놓음
# api.route('/profile')은 '/api/profile'에 매칭되며,
# url_for를 쓸 경우엔 함수명 앞에 블루프린트명인 api. 을 붙여줘야한다. ex) url_for('api.get_posts')
api = Blueprint('api', __name__, template_folder='templates')

@api.route('/profile', methods=['GET'])
def get_profile():
    pass


@api.route('/profile', methods=['PUT'])
def put_profile():
    pass


@api.route('/posts', methods=['GET'])
def get_posts():
    pass


@api.route('/post', method=['POST'])
def write_post():
    pass


@api.route('/post', method=['PUT'])
def put_post():
    pass


@api.route('/post', method=['DELETE'])
def delete_post():
    pass


@api.route('/comments', methods=['GET'])
def get_comments():
    pass


@api.route('/comment', method=['POST'])
def write_comment():
    pass


@api.route('/comment', method=['PUT'])
def put_comment():
    pass


@api.route('/comment', method=['DELETE'])
def delete_comment():
    pass
