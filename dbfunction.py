import pymysql
import config
import bcrypt

# < table 종류 >
# comment = [id, user_id, text, post_id]
# post    = [id, post_text, user_id, image]
# user    = [id, name, login_id, password, profile_image, background_image]

# MySQL db에 접근하는 함수  config.py 파일속 비밀번호를 수정해서 사용하세요
def MySQL_connect():
    db = pymysql.connect(
        host     = config.db['host'], 
        port     = config.db['port'], 
        user     = config.db['user'], 
        password = config.db['password'], 
        db       = config.db['database'], 
        charset  ='utf8')
    return db    


# session_primary_id 를 가진 유저의 comment, post  table 정보를 가져올수있습니다.
# 로그인시 저장 되어있는 session_primary_id 와 찾고자하는 table을 매개변수로 입력할면 됩니다.
def get_user_comment_post(session_primary_id, table):
    db = MySQL_connect() 
    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') 

    cursor.execute(f'SELECT * FROM {table} WHERE id=%s',(session_primary_id))
    user_table_info = cursor.fetchone()
    
    db.commit() 
    db.close()

    return user_table_info


# user table 정보를 가져오는 함수입니다. id, pw 를 input값으로 받아 가져옳수있습니다.
# 유저가 잘못된 ID, PW 입력시 None를 리턴합니다. 
def get_user_table(ID, PW):
    db = MySQL_connect() 
    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') 

    cursor.execute('SELECT * FROM user WHERE login_id=%s',(ID)) 
    user_info = cursor.fetchone()

    db.commit() 
    db.close()

    if user_info is not None:                                                  # None이 아니라는것은 아이디는 맞았을때 라는 뜻이다.
        hashed_password  = user_info['password']                               # (비밀번호 체크) 입력한 아이디가 db에 존재하면 유저의 암호화된 비밀번호를 가져온다.
        checkpw_password = bcrypt.checkpw(PW.encode('utf-8'), hashed_password) # 매개변수로 받은 유저가 입력한 PW를 받아 암호화된 비밀번호를  bcrypt.checkpw()를 통해 대조한다.
        
        if checkpw_password == True:                                           # 그리고 만약 True가 반환되면 (대조시 맞으면 True 틀리면 False다.)유저정보를 반환한다.
            return user_info                                                   # 입력한 아이디가 db에 존재하면 유저의 정보를 가져온다 (비밀번호는 암호화 되어있다.)
        # elif checkpw_password == False:
        #     return None
    else:
        return None                                                            # 입력한 비밀번호가 틀렸다면 if checkpw_password == True: 가 적용되지 않기 때문에
             


# 회원가입시 입력한 값을 MySQL에 저장하는 함수입니다. name - id - pw 순서대로 저장됩니다.(table순서)
def save_user_info(name, ID, PW):
    db = MySQL_connect() 
    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') 
    # 지금은 이건 임시로 사용합니다. 원래는 암호화를 생각해서 처음 부터 table 생성시 VARBINARY(255)로 긴 문자를 받을수있게 해야합니다.
    cursor.execute('ALTER TABLE user MODIFY password VARBINARY(255)') 
    # 사이즈 변경 방법 -- alter table 테이블명 modify 컬럼명 varchar(사이즈);

    password = PW                                  
    salt = bcrypt.gensalt()                        
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)  # 입력받은 PW를 bcrypt.hashpw()를 이용해서 암호화 시킵니다.

    cursor.execute('INSERT INTO user (name, login_id, password) VALUES (%s, %s, %s)', (name, ID, hashed_pw))

    cursor.execute('SELECT name, login_id, password FROM user WHERE login_id=%s AND password=%s',(ID, hashed_pw))
    confirm_saved = cursor.fetchone()['login_id']              # 저장하고난후 잘 저장되었는지 체크하는것. 아이디를 반환.

    db.commit() 
    db.close()

    return confirm_saved

# 회원가입시 이미 회원가입된 ID 인지 체크하는 함수입니다. 
# 매개변수로 입력받은 id 혹은 name , 해당 table 명을 입력하면 db안에 정보가 있는지 체크합니다.
def already_exists_id_name(input_id_name, table_item):
    db = MySQL_connect() 
    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') 

    if table_item == 'name':
        cursor.execute('SELECT name FROM user WHERE name=%s',(input_id_name))

    elif table_item == 'login_id':
        cursor.execute('SELECT login_id FROM user WHERE login_id=%s',(input_id_name))

    confirm_id = cursor.fetchone()

    db.commit() 
    db.close()

    return confirm_id

# 매개변수로 유저의 정보를 받아 MySQL에 유저의 정보를 삭제합니다. ( 회원 탈퇴 ) -------- 미완성.
def delete_user_info(name, ID, PW):
    db = MySQL_connect()
    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') # MySQL 사용가능하게하는

    cursor.execute('DELETE FROM user WHERE name=%s AND login_id=%s AND password=%s',(name, ID, PW))

    cursor.execute('SELECT name, login_id, password FROM user WHERE name=%s AND login_id=%s AND password=%s',(name, ID, PW))
    confirm_deleted = cursor.fetchone()

   # 회원탈퇴 과정 - 회원이 로그인 되어있는 상태에서만 탈퇴 할수있게 세션으로 화면을 가져온다.
   # 삭제를 하면 회원이 작성한 글, 사진 정보 등이 모두 삭제된다는 것을 알려준다.
   # 삭제를 위해 회원 정보 확인을 위해 회원이 입력한 값이 db에 있는지부터 확인하고 정보가 없다면 회원정보를 확인하라는 것을 알린다.
   # 삭제를 하면 회원이 작성한 글, 사진 정보 등이 모두 삭제된다는 것을 알려준다.
   # 정보를 맞게 입력했다면 db에있는 해당 회원의 모든 table을 삭제하도록한다.
    if confirm_deleted is None:
        hide_pw = len(PW) * "*"
        confirm_deleted_msg = f'{name}, {ID}, {str(hide_pw)} 회원정보 삭제'
        confirm_deleted_msg = f'{name}님 회원탈퇴 성공'

    db.commit() 
    db.close()  

    return confirm_deleted_msg 

# MySQL post table 정보를 모두 가져옵니다.
def get_posts_all():
    db = MySQL_connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE hotsix;')

    cursor.execute(f'SELECT * FROM post')
    posts_all = cursor.fetchall()

    db.commit()
    db.close()
    return posts_all


    
#------------------------------실행 예시-------------------------------
# input_id = 'messigod58122'
# input_pw = 'wjd!5810238'
# print(get_user_table(input_id,input_pw))                # 로그인시 사용

# session_primary_id = 1
# post_table    = 'post'
# comment_table = 'comment'
# print(get_user_comment_post(session_primary_id, post_table))
# print(get_user_comment_post(session_primary_id, comment_table))

# input_name = '앙까라메시2'
# input_id   = 'messigod58122'
# input_pw   = 'wjd!5810238'
# print(save_user_info(input_name, input_id, input_pw))    # 회원가입

# print(delete_user_info(input_name, input_id, input_pw))  # 탈퇴

# input_name = '정성훈'
# input_id = 'soo581'
# print(already_exists_id_name(input_name , 'name'))                             # 이름 체크
# print(already_exists_id_name(input_id , 'login_id'))                           # 이름 체크
#------------------------------실행 예시-------------------------------



