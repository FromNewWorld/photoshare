import tornado.web


from utils.account import authenticate,register
from .main import AuthBaseHandler
from models.account import User

class LoginHandler(AuthBaseHandler):
    '''
    登入页面
    '''
    def get(self, *args, **kwargs):
        if self.current_user:                   #如果已经登入，将跳转‘/’
            self.redirect(next)
        next = self.get_argument('next',
                                     '/')  # 若没登入，将会获取next参数，这个参数是由main中页面中的装饰器@tornado.web.authenticated赋予（未登入是访问的页面）
        self.render('login.html',               #到/login页面
                    next=next,
                    )

    def post(self, *args, **kwargs):
        username = self.get_argument('username',None)   #获取账号密码
        password = self.get_argument('password',None)
        passed = authenticate(username,password)    #存在：验证身份
        if passed:                                  #如果身份验证成功
            self.session.set('user_info',username)  #set一个session，内容为username
            User.update_last_login(username)
            next = self.get_argument('next', '/')   #获取下next参数
            self.redirect(next)                     #跳转到next
        else:                                       #验证身份失败：页面打印login fail
            self.write('login fail')


class LogoutHandler(AuthBaseHandler):
    '''
    登出
    '''
    def get(self):
        # self.session.set('user_info','')            #set session为空
        self.session.delete('user_info')
        self.redirect('/login')                     #跳转/login页面


class SignupHandler(AuthBaseHandler):
    '''
    注册
    '''
    def get(self, *args, **kwargs):
        self.render('signup.html',msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username',None)       #获取注册信息
        password1 = self.get_argument('password1',None)
        password2 = self.get_argument('password2',None)
        email = self.get_argument('email',None)
        if username and password1 and password2:
            if password1 != password2:
                self.write('两次密码不同')
            else:
                ret=register(username,password1,email)      #进行注册
                if ret =='ok':                              #如果注册返回值为‘ok’
                    self.session.set('user_info',username)  #进行登入以及跳转
                    self.redirect('/')
                else:                                       #注册失败打印注册返回值
                    self.write(ret)
        else:                                               #username，password1，password2任一个为空，重新跳转注册界面
            self.render('/signup.html',msg='register fail')




