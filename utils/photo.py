import glob
import os
from PIL import Image


def get_imges(path):
    images = glob.glob(path + '/*.jpg')
    # images=[]
    # for file in glob.glob(path + '/[0-9].jpg'):         #获取文件的路径，并以列表输出（此处将获取path路径下名字如*.jpg的文件）
    #     images.append(file)
    return images

def make_thumbnail(path):                                    #在路径下生成缩略图

    file, ext = os.path.splitext(os.path.basename(path))                      #将传入的路径分开，分为路径以及后缀（.jpg）
    im = Image.open(path)
    im.thumbnail((200, 200))                                #生成200x200的缩略图
    im.save("./static/uploads/thumbnails_200x200/{}_{}x{}.jpg".format(file, 200, 200), "JPEG")  #保存在相面划分出来的路径下，名字为（）_200x200的jpg图片


def get_thumbimges(path):
    thumbimages = glob.glob(path + '/*_200x200.jpg')        #获取path路径下文件名类似为  （ ）_200x200.jpg的图片即缩略图
    # for file in glob.glob(path + '/*_200x200.jpg'):  # 获取文件的路径，并以列表输出（此处将获取path路径下名字如*.jpg的文件）
    #     thumbimages.append(file)
    return thumbimages                                      #返回缩略图列表

