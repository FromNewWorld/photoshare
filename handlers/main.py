import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    '''
    Home page
    '''
    def get(self):
        # self.write('ok')
        self.render('index.html')

class ExploreHandler(tornado.web.RequestHandler):
    '''
    Explore page
    '''
    def get(self):
        self.render('explore.html')

class PostHandler(tornado.web.RequestHandler):
    '''
    Post page
    '''
    def get(self,*args,**kwargs):
        print(args)
        print(kwargs)
        self.render('post.html',
                    post_id=kwargs['post_id']
                    )
