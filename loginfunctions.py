import string

class confirm_name_id_pw():

#---------------------------------------------------------------------------

    def confirm_name(name):
        # 가나다라1234 각 문자의 유니코드 코드 값 중에 49(1)은 44032(가)부터 55199(힣) 사이가 를 체크하고
        # 완성된문자의경우 Ture 반대의 경우 False를 반환합니다.
        completed_Korean = all(44032 <= ord(Korean_item) <= 55199 for Korean_item in name)

        if len(name) < 2 or len(name) > 20: 
            return "Name은 2자 이상 20자 이하로 입력 가능합니다."   

        elif completed_Korean != True:
            return "Name을 한글로 완성된 문자로 입력해 주세요."

        else:
            return True

#---------------------------------------------------------------------------

    def confirm_id(ID):
        
        if len(ID) < 5 or len(ID) > 20:                 
            return "ID는 5자 이상 20자 이하, 영어, 숫자만 입력 가능합니다."

        elif not all(char.isalnum() for char in ID):
            return "ID는 영어, 숫자로만 이루어져야 합니다." 
        else:
            return True

#---------------------------------------------------------------------------

    def confirm_pw(PW):
            
        if len(PW) < 8:
            return "Password는 8자 이상이어야 합니다."

        elif not any(char.isdigit() for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."
            
        elif not any(char.isalpha() for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."

        elif not any(char in string.punctuation for char in PW):
            return "Password는 특수문자, 영어, 숫자가 포함되어야 합니다."

        else:  
            return True    

#---------------------------------------------------------------------------

# name = '정성훈'
# ID = 'asdaf'
# PW = 'asfdasasdasd11f!'

# print(confirm_name_id_pw.confirm_name(name))
# print(confirm_name_id_pw.confirm_id(ID))
# print(confirm_name_id_pw.confirm_pw(PW))

