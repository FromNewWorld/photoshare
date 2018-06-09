import hashlib
from models.account import User,session,Post

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

def add_post_for(username , image_url,thumb_url):
    '''
    保存特定用户的图片
    :param username:用户名
    :param image_url:上传图片的保存地址（static下的）
    :param thumb_url:缩略图的保存地址（static下的）
    :return:
    '''
    user = session.query(User).filter_by(name=username).first()
    post =Post(image_url=image_url,thumb_url=thumb_url,user=user)
    session.add(post)
    session.commit()
    return post.id

def get_post_for(username):
    user = session.query(User).filter_by(name=username).first()
    posts = session.query(Post).filter_by(user=user)
    return posts

