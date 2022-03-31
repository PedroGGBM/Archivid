import hashlib
import os
import base64

def hash_password(password, salt:str= None):

    if salt:
        salt = salt.encode('utf-8')
        salt = base64.b64decode(salt)
    else:
        salt = os.urandom(32) # A new salt for this user

    hashed_pwd = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    #str encoding both the hash and salt
    hashed_pwd=  base64.b64encode(hashed_pwd)

    hashed_pwd = hashed_pwd.decode('utf-8')

    salt = base64.b64encode(salt)

    salt = salt.decode('utf-8')

    return hashed_pwd,salt

   

