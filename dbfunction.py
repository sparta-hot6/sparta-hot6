import pymysql
import config

# < table 종류 >
# comment = [id, user_id, text, post_id]
# post    = [id, post_text, user_id, image]
# user    = [id, name, login_id, password, profile_image, background_image]

# user table 정보를 가져오는 함수입니다. id, pw 를 input값으로 받아 가져옳수있습니다.
# 잘못된 유저가 ID, PW 입력시 None를 리턴합니다. 
def get_db_user(ID, PW):
    db = pymysql.connect(
    host     = config.db['host'], 
    port     = config.db['port'], 
    user     = config.db['user'], 
    password = config.db['password'], 
    db       = config.db['database'], 
    charset  ='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor) 
    cursor.execute('USE hotsix;') 

    cursor.execute(f'SELECT * FROM user WHERE login_id=%s AND password=%s',(ID, PW))
    user_info = cursor.fetchone()
    
    db.commit() 
    db.close()

    return user_info

# input_id= 'jmoon581'
# input_pw= '930523'
# print(get_db_user(input_id,input_pw))





#---- 사용 할지 고민중입니다.

    # def login_confirm(input_id, input_pw):
    #     db = Get_db.get_db_user()
    #     id = input_id
    #     pw = input_pw

    #     login_confirm  = 'login fail'
    #     name           = None
    #     PRIMARY_KEY_ID = None
    #     for i in range(len(db)):

    #         if db[i]["login_id"] == id and db[i]["password"] == pw:
    #             login_confirm  = "login succed"
    #             name           = db[i]["name"]
    #             PRIMARY_KEY_ID = db[i]["id"]
    #         elif db[i]["login_id"] == id and db[i]["password"] != pw:  
    #             login_confirm = "worng password"   
                
    #         # elif db[i]["login_id"] != id and db[i]["password"] == pw:  
    #         #     login_confirm = "check your id"

    #     return [name, login_confirm, PRIMARY_KEY_ID]

# # input_id = "soo581"
# # input_pw = "9811"

# # print(Get_db.login_confirm(input_id,input_pw))
#---- 사용 할지 고민중입니다.