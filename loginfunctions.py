import string

class confirm_name_id_pw():
    
    def confirm_name(name):
        # 가나다라1234 각 문자의 유니코드 코드 값 중에 49(1)은 44032(가)부터 55199(힣) 사이가 를 체크하고
        # 완성된문자의경우 Ture 반대의 경우 False를 반환합니다.
        completed_Korean = all(44032 <= ord(Korean_item) <= 55199 for Korean_item in name)

        if name == "":
            return "Name을 입력해주세요"

        elif len(name) < 2 or len(name) > 20: # 영어 혹은 한글이 아니면 False를 반환
            return "Name은 5자 이상 20자 이하로 입력 가능합니다."

        elif completed_Korean != True:
            return "Name을 한글로 작성할 경우 완성된 문자로 입력해 주세요."

        elif name.isalpha() == False:
            return "Name은 한글, 영어로 입력 가능하며 공백을 넣을수 없습니다."

        else:
            return True

    def confirm_id(ID):
        if ID == "":
            return "ID를 입력해주세요"

        elif len(ID) < 5 or len(ID) > 20: # 문자길이를 제한합니다. 영어,숫자만 입력할수있습니다.
            return "ID는 5자 이상 20자 이하, 영어, 숫자만 입력 가능합니다."

        elif ID.isalnum() == False:
            return "ID는 한글, 영어만 입력 가능합니다."
        
        else:
            return True

    def confirm_pw(PW):
        if PW == "":
            return "Password를 입력해주세요"    

        elif len(PW) < 8:
            return "Password는 8자 이상이어야 합니다.."

        elif not any(char.isdigit() for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."
            
        elif not any(char.isalpha() for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."

        elif not any(char in string.punctuation for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."

        else:  
            return True    



# name = '정성훈'
# ID = ''
# PW = ''

# print(confirm_name_id_pw.confirm_name(name))
# print(confirm_name_id_pw.confirm_id(ID))
# print(confirm_name_id_pw.confirm_pw(PW))



# if len(input_name) < 5 or len(input_name) > 20: # 영어 혹은 한글이 아니면 False를 반환
#             return render_template('signup.html', confirm_name_msg="Name을 5자 이상 20자 이하로 작성해주세요")
#         elif input_name.isalpha() == False:
#             return render_template('signup.html', confirm_name_msg="Name을 한글, 영어로만 작성해주세요.")

#         if len(input_id) < 5 or len(input_id) > 20: # 문자길이를 제한합니다. 영어,숫자만 입력할수있습니다.
#             return render_template('signup.html', confirm_id_msg="ID는 5자 이상 20자 이하, 영어, 숫자만 입력가능합니다.")
#         elif input_id.isalnum() == False:
#             return render_template('signup.html', confirm_name_msg="Name을 한글, 영어로만 작성해주세요.")
    
#         if len(input_pw) < 8:
#             return render_template('signup.html', message="Password는 8자 이상이여야합니다.")
#         elif not any(char.isdigit() for char in input_pw):
#             return render_template('signup.html', message="Password는 특수문자, 영어, 숫자가 포함되어야합니다.")
#         elif not any(char.isalpha() for char in input_pw):
#             return render_template('signup.html', message="Password는 특수문자, 영어, 숫자가 포함되어야합니다.")
#         elif not any(char in string.punctuation for char in input_pw):
#             return render_template('signup.html', message="Password는 특수문자, 영어, 숫자가 포함되어야합니다.")
#         else:  