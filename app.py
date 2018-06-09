import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options


from handlers import main,auth


define('port',default='8000',help='Listening port',type=int)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',main.IndexHandler),
            (r'/explore',main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
            (r'/upload',main.UploadHandler),
            (r'/login', auth.LoginHandler),
            (r'/logout', auth.LogoutHandler),
            (r'/signup', auth.SignupHandler),
        ]
        settings = dict(
            debug='True',
            template_path='templates',
            static_path='static',
            login_url = '/login',                   #与@tornado.web.authenticated（验证有无get_current_user）相关，如果验证不通过（无），将会跳转到/login
            cookie_secret='asdvzxgfqwe',
            pycket={
                'engine':'redis',
                'storage':{
                    'host':'127.0.0.1',
                    'port':6379,
                    'db_sessions':5,
                    'db_notifications':11,
                    'max_connections':2 ** 30,
                },
                'cookies':{
                    'expires_days':30,
                },
            }
        )

        super(Application,self).__init__(handlers,**settings)



application = Application()

if __name__=='__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Serves start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()


