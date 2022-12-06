from flask import Blueprint, session, request
import pymysql
from pymysql.cursors import DictCursor
from upload import upload_file, download_file
from dbfunction import MySQL_connect

# api Blueprint를 main에 url_prefix를 /api로 등록시켜놓음
# api.route('/profile')은 '/api/profile'에 매칭되며,
# url_for를 쓸 경우엔 함수명 앞에 블루프린트명인 api. 을 붙여줘야한다. ex) url_for('api.get_posts')
api = Blueprint('api', __name__, template_folder='templates')


@api.route('/profile', methods=['GET'])
def get_profile():
    if "PRIMARY_KEY_ID" not in session:
        return
    user_id = session["PRIMARY_KEY_ID"]
    sql = f"""
    SELECT id, name, login_id, profile_image, background_image
    FROM user
    WHERE id = {user_id}
    """
    db = MySQL_connect()
    cursor = db.cursor(DictCursor)
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data


@api.route('/profile', methods=['PUT'])
def put_profile():
    if "PRIMARY_KEY_ID" not in session:
        return 'none'
    db = MySQL_connect()
    cursor = db.cursor()
    user_id = session["PRIMARY_KEY_ID"]
    setquery = ''
    if 'pf_name' in request.form:
        name = request.form['pf_name']
        setquery = setquery + \
            f", name = {name}" if setquery else f"name = {name}"
    if 'pf_img' in request.files:
        pf_img = upload_file(request.files['pf_img'])
        setquery = setquery + \
            f", profile_image = '{pf_img}'" if setquery else f"profile_image = '{pf_img}'"
    if 'bg_img' in request.files:
        bg_img = upload_file(request.files['bg_img'])
        setquery = setquery + \
            f", background_image = '{bg_img}'" if setquery else f"background_image = '{bg_img}'"
    if setquery:
        sql = f"""
      UPDATE user
      SET {setquery}
      WHERE id = {user_id}
      """
        cursor.execute(sql)
        db.commit()
    db.close()
    return 'success'


@api.route('/file/<filename>', methods=['GET'])
def download_files(filename):
    return download_file(filename)


@api.route('/posts', methods=['GET'])
def get_posts():
    db = MySQL_connect()
    cursor = db.cursor(DictCursor)
    sql = """
    SELECT *
    FROM post
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data


@api.route('/post', methods=['POST'])
def write_post():
    if 'PRIMARY_KEY_ID' not in session:
        return 'none'
    db = MySQL_connect()
    cursor = db.cursor()
    user_id = session['PRIMARY_KEY_ID']
    text = request.form['text']
    if 'img' in request.files:
        img = upload_file(request.files['img'])
    else:
        img = ''
    sql = f"""
    INSERT INTO post (post_text, user_id, image)
    VALUES ('{text}', {user_id}, '{img}')
    """
    cursor.execute(sql)
    db.commit()
    db.close()
    return 'success'


@api.route('/post', methods=['PUT'])
def put_post():
    if 'PRIMARY_KEY_ID' not in session:
        return 'none'
    db = MySQL_connect()
    cursor = db.cursor()
    user_id = session['PRIMARY_KEY_ID']
    post_id = request.form['post_id']
    text = request.form['text']
    setquery = f"post_text = '{text}'"
    if 'img' in request.files:
        img = upload_file(request.files['img'])
        setquery += f", image='{img}'"
    sql = f"""
    UPDATE post
    SET {setquery}
    WHERE id = {post_id}, user_id = {user_id}
    """
    cursor.execute(sql)
    db.commit()
    db.close()
    return 'success'


@api.route('/post', methods=['DELETE'])
def delete_post():
    if 'PRIMARY_KEY_ID' not in session:
        return 'none'
    db = MySQL_connect()
    cursor = db.cursor()
    user_id = session['PRIMARY_KEY_ID']
    post_id = request.form['post_id']
    sql = f"""
    DELETE
    FROM post
    WHERE id = {post_id}, user_id = {user_id}
    """
    cursor.execute(sql)
    db.commit()
    db.close()
    return 'success'


@api.route('/comments', methods=['GET'])
def get_comments():
    pass


@api.route('/comment', methods=['POST'])
def write_comment():
    pass


@api.route('/comment', methods=['PUT'])
def put_comment():
    pass


@api.route('/comment', methods=['DELETE'])
def delete_comment():
    pass
