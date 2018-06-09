import tornado.web


from utils import account
from .main import AuthBaseHandler

class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        next = self.get_argument('next', '/')
        self.render('login.html',
                    next=next,
                    )

    def post(self, *args, **kwargs):
        username = self.get_argument('username',None)
        password = self.get_argument('password',None)

        passed = account.authenticate(username,password)

        if passed:
            self.session.set('user_info',username)
            next = self.get_argument('next', '/')
            self.redirect(next)
        else:
            self.write('login fail')


class LogoutHandler(AuthBaseHandler):
    def get(self):
        self.session.set('user_info','')
        self.redirect('/login')


class SignupHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('signup.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username',None)
        password1 = self.get_argument('password1',None)
        password2 = self.get_argument('password2',None)
        email = self.get_argument('email',None)
        if username and password1 and password2:
            if password1 != password2:
                self.write('两次密码不同')
            else:
                pass



