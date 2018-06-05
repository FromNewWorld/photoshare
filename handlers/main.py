import tornado.web
import os



from utils import photo

class IndexHandler(tornado.web.RequestHandler):
    '''
    Home page
    '''
    def get(self,*args,**kwargs):
        images_path = os.path.join(self.settings.get('static_path'),'uploads')  #图片的路径--static_path+upload（statci_path路径在Application里定义）
        print(images_path)
        images = photo.get_imges(images_path)                                   #一个jpg图片路径的列表
        print(images)
        self.render('index.html',images = images)


class ExploreHandler(tornado.web.RequestHandler):
    '''
    Explore page
    '''
    def get(self,*args,**kwargs):
        thumb = photo.get_thumbimges('./static/uploads/thumbnails_200x200')       #一个缩略图图片路径的列表
        self.render('explore.html',
                    thumb=thumb,
                    )

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
