import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo,account
from utils.account import add_post_for,get_post_for

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        '''
        :return: 返回用户信息
        '''
        return self.session.get('user_info')          #获取user_info，user_info的内容为username（auth中的login里设置的）

class IndexHandler(AuthBaseHandler):
    '''
    Home page
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        # images_path = os.path.join(self.settings.get('static_path'),'uploads')  #图片的路径--static_path+upload（statci_path路径在Application里定义）
        # images = photo.get_imges(images_path)                                   #一个jpg图片路径的列表
        posts = get_post_for(self.current_user)                 #current_user是get_current_user不为空时，则返回get_current_user
        image_urls =[p.image_url for p in posts]
        next = self.get_argument('next', '')
        self.render('index.html',images = image_urls,next=next)


class ExploreHandler(AuthBaseHandler):
    '''
    Explore page
    '''

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        posts = get_post_for(self.current_user)
        thumb_urls =[p.thumb_url for p in posts]

        next = self.get_argument('next','')
        self.render('explore.html',
                    thumb=thumb_urls,
                    next=next,
                    )

class PostHandler(tornado.web.RequestHandler):
    '''
    Post page
    '''

    # @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('post.html',
                    post_id=kwargs['post_id'],

                    )


class UploadHandler(AuthBaseHandler):
    '''
    upload to the share of photo
    '''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        next = self.get_argument('next','')
        self.render('upload.html',next=next)

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newing',None)
        for img in img_files:
            saver = photo.ImageSave(self.settings['static_path'],img['filename'])
            saver.save_upload(img['body'])
            saver.make_thumb()

            add_post_for(self.current_user ,saver.upload_url ,saver.thumb_url)
            print('save to {}'.format(saver.upload_path))

        self.render('upload.html')