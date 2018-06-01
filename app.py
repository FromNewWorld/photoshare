import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handlers import main


define('port',default='8000',help='Listening port',type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',main.IndexHandler),
            (r'/explore',main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
        ]
        settings = dict(
            debug='True',
            template_path='templates'
        )

        super(Application,self).__init__(handlers,**settings)



application = Application()

if __name__=='__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Serves start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()


