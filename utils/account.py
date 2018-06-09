USER_DATA={
    'name':'abc',
    'password':'1'
}



def authenticate(username,password):
    if username and password:
        if username == USER_DATA['name'] and password == USER_DATA['password']:
            return True

    return False
