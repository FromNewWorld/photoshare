import hashlib
from models.account import User

def hash_it(password):          #进行hash，返回hash后的值
    return hashlib.md5(password.encode('utf8')).hexdigest()

# USER_DATA={
#     'name':'abc',
#     'password':hash_it('1')
# }


def authenticate(username,password):
    '''
    进行身份验证
    :param username: 用户名
    :param password: 密码
    :return: 返回身份是否正确
    '''
    if username and password:
        if User.get_password(username) and hash_it(password) == User.get_password(username):#
            return True
    return False

def register(name,password,email):
    '''
    注册
    :param name: 用户名
    :param password: 密码
    :param email: 邮箱
    :return: ok/user is exists
    '''
    if User.exists_it(name):
        return 'user is exists'

    pw=hash_it(password)
    print(name,pw,password)
    User.add_user(name,pw,email)
    return 'ok'



