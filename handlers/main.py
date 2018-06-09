import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo,account
from utils.account import add_post_for,get_post_for

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('user_info')

class IndexHandler(AuthBaseHandler):
    '''
    Home page
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        # images_path = os.path.join(self.settings.get('static_path'),'uploads')  #图片的路径--static_path+upload（statci_path路径在Application里定义）
        # images = photo.get_imges(images_path)                                   #一个jpg图片路径的列表
        posts = get_post_for(self.current_user)
        image_urls =[p.image_url for p in posts]
        self.render('index.html',images = image_urls)


class ExploreHandler(AuthBaseHandler):
    '''
    Explore page
    '''

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        posts = get_post_for(self.current_user)
        thumb_urls =[p.thumb_url for p in posts]

        nextname = self.get_argument('next','')
        self.render('explore.html',
                    thumb=thumb_urls,
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


class UploadHandler(AuthBaseHandler):
    '''
    upload to the share of photo
    '''
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img_file in img_files:
            image_url = 'uploads/' + img_file['filename']
            save_to = os.path.join(self.settings['static_path'],image_url)

            # with open('./static/uploads/'+img_file['filename'],'wb') as f:         #上传图片到./static/uploads/目录下
            with open(save_to, 'wb') as f:
                f.write(img_file['body'])
            self.write({'got file': img_file['filename']})
            full_path = photo.make_thumbnail(save_to)          #生成上传图片的缩略图
            thumb_url = os.path.relpath(full_path,self.settings['static_path'])     #缩略图的static下的路径
            add_post_for(self.current_user ,image_url ,thumb_url )