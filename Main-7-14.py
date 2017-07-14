# 常用第三方模块
#
# 除了内建的模块外，Python还有大量的第三方模块。
# 基本上，所有的第三方模块都会在PyPI - the Python Package Index上注册，只要找到对应的模块名字，即可用pip安装。

# PIL
# PIL：Python Imaging Library，已经是Python平台事实上的图像处理标准库了。PIL功能非常强大，但API却非常简单易用。
# 由于PIL仅支持到Python 2.7，加上年久失修，于是一群志愿者在PIL的基础上创建了兼容的版本，名字叫Pillow，支持最新Python 3.x，
# 又加入了许多新特性，因此，我们可以直接安装使用Pillow。
# 安装Pillow
# 在命令行下直接通过pip安装：
# $ pip install pillow
# 如果遇到Permission denied安装失败，请加上sudo重试。

# 操作图像
# 来看看最常见的图像缩放操作，只需三四行代码：
# from PIL import Image
# # 打开一个jpg图像文件，注意是当前路径:
# im = Image.open('test.jpg')
# # 获得图像尺寸:
# w, h = im.size
# print('Original image size: %sx%s' % (w, h))
# # 缩放到50%:
# im.thumbnail((w//2, h//2))
# print('Resize image to: %sx%s' % (w//2, h//2))
# # 把缩放后的图像用jpeg格式保存:
# im.save('thumbnail.jpg', 'jpeg')
# 其他功能如切片、旋转、滤镜、输出文字、调色板等一应俱全。
#
# 比如，模糊效果也只需几行代码：
# from PIL import Image, ImageFilter
#
# # 打开一个jpg图像文件，注意是当前路径
# im = Image.open('test.jpg')
# # 应用模糊滤镜:
# im2 = im.filter(ImageFilter.BLUR)
# im2.save('blur.jpg', 'jpeg')

# PIL的ImageDraw提供了一系列绘图方法，让我们可以直接绘图。比如要生成字母验证码图片：
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random


# 随机字母
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


# 240 * 60
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('arial.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), fill=rndColor2(), font=font)
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
# 要详细了解PIL的强大功能，请请参考Pillow官方文档：
# https://pillow.readthedocs.org/
# 小结
# PIL提供了操作图像的强大功能，可以通过简单的代码完成复杂的图像处理。



# virtualenv

# 在开发Python应用程序的时候，系统安装的Python3只有一个版本：3.4。所有第三方的包都会被pip安装到Python3的site-packages目录下。
#
# 如果我们要同时开发多个应用程序，那这些应用程序都会共用一个Python，就是安装在系统的Python 3。如果应用A需要jinja 2.7，而应用B需要jinja 2.6怎么办？
#
# 这种情况下，每个应用可能需要各自拥有一套“独立”的Python运行环境。virtualenv就是用来为一个应用创建一套“隔离”的Python运行环境。
#
# 首先，我们用pip安装virtualenv：
# $ pip3 install virtualenv
# 然后，假定我们要开发一个新的项目，需要一套独立的Python运行环境，可以这么做：
#
# 第一步，创建目录：
#
# Mac:~ michael$ mkdir myproject
# Mac:~ michael$ cd myproject/
# Mac:myproject michael$
# 第二步，创建一个独立的Python运行环境，命名为venv：
#
# Mac:myproject michael$ virtualenv --no-site-packages venv
# Using base prefix '/usr/local/.../Python.framework/Versions/3.4'
# New python executable in venv/bin/python3.4
# Also creating executable in venv/bin/python
# Installing setuptools, pip, wheel...done.
# 命令virtualenv就可以创建一个独立的Python运行环境，我们还加上了参数--no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。
#
# 新建的Python环境被放到当前目录下的venv目录。有了venv这个Python环境，可以用source进入该环境：
#
# Mac:myproject michael$ source venv/bin/activate
# (venv)Mac:myproject michael$
# 注意到命令提示符变了，有个(venv)前缀，表示当前环境是一个名为venv的Python环境。
#
# 下面正常安装各种第三方包，并运行python命令：
#
# (venv)Mac:myproject michael$ pip install jinja2
# ...
# Successfully installed jinja2-2.7.3 markupsafe-0.23
# (venv)Mac:myproject michael$ python myapp.py
# ...
# 在venv环境下，用pip安装的包都被安装到venv这个环境下，系统Python环境不受任何影响。也就是说，venv环境是专门针对myproject这个应用创建的。
#
# 退出当前的venv环境，使用deactivate命令：
#
# (venv)Mac:myproject michael$ deactivate
# Mac:myproject michael$
# 此时就回到了正常的环境，现在pip或python均是在系统Python环境下执行。
#
# 完全可以针对每个应用创建独立的Python运行环境，这样就可以对每个应用的Python环境进行隔离。
#
# virtualenv是如何创建“独立”的Python运行环境的呢？原理很简单，就是把系统Python复制一份到virtualenv的环境，用命令source venv/bin/activate进入一个virtualenv环境时，virtualenv会修改相关环境变量，让命令python和pip均指向当前的virtualenv环境。
#
# 小结
#
# virtualenv为应用提供了隔离的Python运行环境，解决了不同应用间多版本的冲突问题
