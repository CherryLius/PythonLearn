# 文件读写
# 读文件
# 要以读文件的模式打开一个文件对象，使用Python内置的open()函数，传入文件名和标示符
f = open('Main-7-6.py', 'r', encoding='utf-8')
# 标示符'r'表示读，这样，我们就成功地打开了一个文件。
# 如果文件不存在，open()函数就会抛出一个IOError的错误，并且给出错误码和详细的信息告诉你文件不存在
# 如果文件打开成功，接下来，调用read()方法可以一次读取文件的全部内容，
# Python把内容读到内存，用一个str对象表示
s = f.read()
print(s)
f.close()
# 最后一步是调用close()方法关闭文件。
# 文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，
# 并且操作系统同一时间能打开的文件数量也是有限的

# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现
try:
    f = open('Main-7-6.py', 'r', encoding='utf-8')
    print(f.read())
finally:
    if f:
        f.close()
# 但是每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法
with open('Main-7-6.py', 'r', encoding='utf-8') as f:
    print(f.read())
# 这和前面的try ... finally是一样的，但是代码更佳简洁，并且不必调用f.close()方法

# 调用read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了，
# 所以，要保险起见，可以反复调用read(size)方法，每次最多读取size个字节的内容。
# 另外，调用readline()可以每次读取一行内容，
# 调用readlines()一次读取所有内容并按行返回list。

# 如果文件很小，read()一次性读取最方便；
# 如果不能确定文件大小，反复调用read(size)比较保险；
# 如果是配置文件，调用readlines()最方便
with open('Main-7-6.py', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        print(line.strip())

# file-like Object
# 像open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object。
# 除了file外，还可以是内存的字节流，网络流，自定义流等等。
# file-like Object不要求从特定类继承，只要写个read()方法就行。
# StringIO就是在内存中创建的file-like Object，常用作临时缓冲


# 二进制文件
# 前面讲的默认都是读取文本文件，并且是UTF-8编码的文本文件。
# 要读取二进制文件，比如图片、视频等等，用'rb'模式打开文件即可
f = open('Main-7-6.py', 'rb')
print(f.read())

# 字符编码
# 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数，例如，读取GBK编码的文件：
# >>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
# >>> f.read()
# '测试'

# 遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError，
# 因为在文本文件中可能夹杂了一些非法编码的字符。
# 遇到这种情况，open()函数还接收一个errors参数，表示如果遇到编码错误后如何处理。
# 最简单的方式是直接忽略：
# >>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')
f = open('Main-7-6.py', 'r', errors='ignore')
print(f.read())

# 写文件
# 写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件：
# >>> f = open('/Users/michael/test.txt', 'w')
# >>> f.write('Hello, world!')
# >>> f.close()
# 你可以反复调用write()来写入文件，但是务必要调用f.close()来关闭文件。当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。忘记调用close()的后果是数据可能只写了一部分到磁盘，剩下的丢失了。所以，还是用with语句来得保险：
# with open('/Users/michael/test.txt', 'w') as f:
#     f.write('Hello, world!')
# 要写入特定编码的文本文件，请给open()函数传入encoding参数，将字符串自动转换成指定编码
# 在Python中，文件读写是通过open()函数打开的文件对象完成的。使用with语句操作文件IO是个好习惯

# StringIO
# 很多时候，数据读写不一定是文件，也可以在内存中读写。
# StringIO顾名思义就是在内存中读写str。
# 要把str写入StringIO，我们需要先创建一个StringIO，然后，像文件一样写入即可
from io import StringIO

f = StringIO()
print(f.write('Hello'))
# getvalue()方法用于获得写入后的str
print(f.getvalue())

# 要读取StringIO，可以用一个str初始化StringIO，然后，像读文件一样读取
f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f.readline()
    if not s:
        break
    print(s.strip())

# BytesIO
# StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
# BytesIO实现了在内存中读写bytes，我们创建一个BytesIO，然后写入一些bytes
from io import BytesIO

f = BytesIO()
f.write('中文'.encode('utf-8'))
print(f.getvalue())
# 写入的不是str，而是经过UTF-8编码的bytes。
# 和StringIO类似，可以用一个bytes初始化BytesIO，然后，像读文件一样读取
f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f.read())

# 操作文件和目录
#
# 如果我们要操作文件、目录，可以在命令行下面输入操作系统提供的各种命令来完成。比如dir、cp等命令。
# 如果要在Python程序中执行这些目录和文件的操作怎么办？其实操作系统提供的命令只是简单地调用了操作系统提供的接口函数，Python内置的os模块也可以直接调用操作系统提供的接口函数。
# 打开Python交互式命令行，我们来看看如何使用os模块的基本功能
import os

print(os.name)
# 要获取详细的系统信息，可以调用uname()函数
# print(os.uname())
# 注意uname()函数在Windows上不提供，也就是说，os模块的某些函数是跟操作系统相关的

# 环境变量
# 在操作系统中定义的环境变量，全部保存在os.environ这个变量中，可以直接查看
print(os.environ)
# 要获取某个环境变量的值，可以调用os.environ.get('key')：
print(os.environ.get('PATH'))
print(os.environ.get('x', 'default'))
# 操作文件和目录

# 操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，
# 这一点要注意一下。查看、创建和删除目录可以这么调用
# 查看当前目录的绝对路径:
print(os.path.abspath('.'))
# # 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
print(os.path.join('F:\Python\work\learn-demo', 'test'))
# # 然后创建一个目录:
# os.mkdir(r'F:\Python\work\learn-demo\test')
# # 删掉一个目录:
# os.rmdir(r'F:\Python\work\learn-demo\test')
# 把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符

# 同样的道理，要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数，
# 这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名
print(os.path.split('F:\Python\work\learn-demo\Main-7-6.py'))
# os.path.splitext()可以直接让你得到文件扩展名
print(os.path.splitext('F:\Python\work\learn-demo\Main-7-6.py'))
