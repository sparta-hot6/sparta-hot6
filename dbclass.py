import pymysql

class Get_db():

    def get_db_user():
        db = pymysql.connect(host="localhost2", port=3306, user='root', passwd='gksehdwn123, db='hotsix', charset='utf8')
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute('USE hotsix;') 
        # cursor.execute(f"SELECT login_id, password, name FROM user WHERE login_id = '{id}' and '{pw}'")
        # db = cursor.fetchall()
        cursor.execute(f"SELECT * FROM user;")
        user_db = cursor.fetchall()

        db.commit() 
        db.close()

        return user_db

    def login_confirm(input_id, input_pw):
        db = Get_db.get_db_user()
        id = input_id
        pw = input_pw

        login_confirm = 'login fail'
        name          = None

        for i in range(len(db)):

            if db[i]["login_id"] == id and db[i]["password"] == pw:
                login_confirm = "login succed"
                name          = db[i]["name"]
                
            elif db[i]["login_id"] == id and db[i]["password"] != pw:  
                login_confirm = "worng password"   
                
            # elif db[i]["login_id"] != id and db[i]["password"] == pw:  
            #     login_confirm = "check your id"

        return [name, login_confirm]
    def get_db_post():
        db = pymysql.connect(host="localhost", port=3306, user='root', passwd='gks1004*', db='hotsix', charset='utf8')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute('USE hotsix;')
        cursor.execute(f"SELECT * FROM post;")
        post_db = cursor.fetchall()
        db.commit()
        db.close()
        return post_db
    # input_id = "soo581"
# input_pw = "9811"

# print(Get_db.login_confirm(input_id,input_pw))