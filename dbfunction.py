import logging

import pymysql
import config


# < table 종류 >
# comment = [id, user_id, text, post_id]
# post    = [id, post_text, user_id, image]
# user    = [id, name, login_id, password, profile_image, background_image]

# MySQL db에 접근하는 함수  config.py 파일속 비밀번호를 수정해서 사용하세요
def MySQL_connect():
    db = pymysql.connect(
        host=config.db['host'],
        port=config.db['port'],
        user=config.db['user'],
        password=config.db['password'],
        db=config.db['database'],
        charset='utf8')
    return db


# session_primary_id 를 가진 유저의 comment, post  table 정보를 가져올수있습니다.
# 로그인시 저장 되어있는 session_primary_id 와 찾고자하는 table을 매개변수로 입력할면 됩니다.
def get_user_comment_post(session_primary_id, table):
    db = MySQL_connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE hotsix;')

    cursor.execute(f'SELECT * FROM {table} WHERE id=%s', (session_primary_id))
    user_table_info = cursor.fetchone()

    db.commit()
    db.close()

    return user_table_info


# user table 정보를 가져오는 함수입니다. id, pw 를 input값으로 받아 가져옳수있습니다.
# 잘못된 유저가 ID, PW 입력시 None를 리턴합니다. 
def get_user_table(ID, PW):
    db = MySQL_connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE hotsix;')

    cursor.execute(f'SELECT * FROM user WHERE login_id=%s AND password=%s', (ID, PW))
    user_info = cursor.fetchone()

    db.commit()
    db.close()

    return user_info


def get_posts_all():
    db = MySQL_connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE hotsix;')

    cursor.execute(f'SELECT * FROM post as p left join `user` as u on p.user_id = u.id')
    posts_all = cursor.fetchall()

    db.commit()
    db.close()

    return posts_all

# ------------------------------실행 예시-------------------------------
# input_id= 'jmoon581'
# input_pw= '930523'
# print(get_user_table(input_id,input_pw))

# session_primary_id = 1
# post_table    = 'post'
# comment_table = 'comment'
# print(get_user_comment_post(session_primary_id, post_table))
# print(get_user_comment_post(session_primary_id, comment_table))
# ------------------------------실행 예시-------------------------------
