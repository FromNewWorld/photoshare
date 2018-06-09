import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo,account

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('user_info')

class IndexHandler(AuthBaseHandler):
    '''
    Home page
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        images_path = os.path.join(self.settings.get('static_path'),'uploads')  #图片的路径--static_path+upload（statci_path路径在Application里定义）
        images = photo.get_imges(images_path)                                   #一个jpg图片路径的列表
        self.render('index.html',images = images)


class ExploreHandler(AuthBaseHandler):
    '''
    Explore page
    '''

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        thumb = photo.get_thumbimges('./static/uploads/thumbnails_200x200')       #一个缩略图图片路径的列表
        nextname = self.get_argument('next','')
        print(nextname)
        self.render('explore.html',
                    thumb=thumb,
                    next=nextname,
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


class UploadHandler(tornado.web.RequestHandler):
    '''
    upload to the share of photo
    '''
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img_file in img_files:
            with open('./static/uploads/'+img_file['filename'],'wb') as f1:         #上传图片到./static/uploads/目录下
                f1.write(img_file['body'])
            self.write({'got file': img_file['filename']})

            photo.make_thumbnail('./static/uploads/'+img_file['filename'])          #生成上传图片的缩略图
