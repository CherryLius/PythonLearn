# hashlib
# 摘要算法简介
# Python的hashlib提供了常见的摘要算法，如MD5，SHA1等等。
# 什么是摘要算法呢？摘要算法又称哈希算法、散列算法。它通过一个函数，把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）。
# 举个例子，你写了一篇文章，内容是一个字符串'how to use python hashlib - by Michael'，并附上这篇文章的摘要是'2d73d4f15c0db7f5ecb321b6a65e5d6d'。
# 如果有人篡改了你的文章，并发表为'how to use python hashlib - by Bob'，你可以一下子指出Bob篡改了你的文章，
# 因为根据'how to use python hashlib - by Bob'计算出的摘要不同于原始文章的摘要。
# 可见，摘要算法就是通过摘要函数f()对任意长度的数据data计算出固定长度的摘要digest，目的是为了发现原始数据是否被人篡改过。
# 摘要算法之所以能指出数据是否被篡改过，就是因为摘要函数是一个单向函数，计算f(data)很容易，但通过digest反推data却非常困难。
# 而且，对原始数据做一个bit的修改，都会导致计算出的摘要完全不同。
# 我们以常见的摘要算法MD5为例，计算出一个字符串的MD5值：
import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
# 如果数据量很大，可以分块多次调用update()，最后计算的结果是一样的：
md5 = hashlib.md5()
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
# 试试改动一个字母，看看计算的结果是否完全不同。
# MD5是最常见的摘要算法，速度很快，生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示。
# 另一种常见的摘要算法是SHA1，调用SHA1和调用MD5完全类似：
sha1 = hashlib.sha1()
sha1.update('how to use sha1 in '.encode('utf-8'))
sha1.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())
# SHA1的结果是160 bit字节，通常用一个40位的16进制字符串表示。
# 比SHA1更安全的算法是SHA256和SHA512，不过越安全的算法不仅越慢，而且摘要长度更长。
# 有没有可能两个不同的数据通过某个摘要算法得到了相同的摘要？
# 完全有可能，因为任何摘要算法都是把无限多的数据集合映射到一个有限的集合中。这种情况称为碰撞，
# 比如Bob试图根据你的摘要反推出一篇文章'how to learn hashlib in python - by Bob'，
# 并且这篇文章的摘要恰好和你的文章完全一致，这种情况也并非不可能出现，但是非常非常困难

# 摘要算法应用
# 摘要算法能应用到什么地方？举个常用例子：
# 任何允许用户登录的网站都会存储用户登录的用户名和口令。如何存储用户名和口令呢？方法是存到数据库表中：
#
# name    | password
# --------+----------
# michael | 123456
# bob     | abc999
# alice   | alice2008
# 如果以明文保存用户口令，如果数据库泄露，所有用户的口令就落入黑客的手里。此外，网站运维人员是可以访问数据库的，也就是能获取到所有用户的口令。
# 正确的保存口令的方式是不存储用户的明文口令，而是存储用户口令的摘要，比如MD5：
#
# username | password
# ---------+---------------------------------
# michael  | e10adc3949ba59abbe56e057f20f883e
# bob      | 878ef96e86145580c38c87f0410ad153
# alice    | 99b1c2188db85afee403b1536010c2c9
# 当用户登录时，首先计算用户输入的明文口令的MD5，然后和数据库存储的MD5对比，如果一致，说明口令输入正确，如果不一致，口令肯定错误。
import hashlib


def get_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


assert 'e10adc3949ba59abbe56e057f20f883e' == get_md5('123456'), get_md5('123456')
assert '878ef96e86145580c38c87f0410ad153' == get_md5('abc999'), get_md5('abc999')
assert '99b1c2188db85afee403b1536010c2c9' == get_md5('alice2008'), get_md5('alice2008')

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}


def login(user, password):
    if user not in db:
        raise KeyError('%s is no exist.' % user)
    else:
        md5_password = get_md5(password)
        if db[user] == md5_password:
            print('%s Login success.' % user)
        else:
            raise ValueError('password wrong.')


login('michael', '123456')
login('bob', 'abc999')
login('alice', 'alice2008')


# login('alice1', 'alice2008')

# 采用MD5存储口令是否就一定安全呢？也不一定。假设你是一个黑客，已经拿到了存储MD5口令的数据库，如何通过MD5反推用户的明文口令呢？暴力破解费事费力，真正的黑客不会这么干。
# 考虑这么个情况，很多用户喜欢用123456，888888，password这些简单的口令，于是，黑客可以事先计算出这些常用口令的MD5值，得到一个反推表：
#
# 'e10adc3949ba59abbe56e057f20f883e': '123456'
# '21218cca77804d2ba1922c33e0151105': '888888'
# '5f4dcc3b5aa765d61d8327deb882cf99': 'password'
# 这样，无需破解，只需要对比数据库的MD5，黑客就获得了使用常用口令的用户账号。
# 对于用户来讲，当然不要使用过于简单的口令。但是，我们能否在程序设计上对简单口令加强保护呢？
# 由于常用口令的MD5值很容易被计算出来，所以，要确保存储的用户口令不是那些已经被计算出来的常用口令的MD5，这一方法通过对原始口令加一个复杂字符串来实现，俗称“加盐”：
def calc_md5(password):
    return get_md5(password + 'the-Salt')


# 经过Salt处理的MD5口令，只要Salt不被黑客知道，即使用户输入简单口令，也很难通过MD5反推明文口令。
# 但是如果有两个用户都使用了相同的简单口令比如123456，在数据库中，将存储两条相同的MD5值，这说明这两个用户的口令是一样的。有没有办法让使用相同口令的用户存储不同的MD5呢？
# 如果假定用户无法修改登录名，就可以通过把登录名作为Salt的一部分来计算MD5，从而实现相同口令的用户也存储不同的MD5。
db = {}


def register(username, password):
    db[username] = get_md5(password + username + 'the-Salt')


def login(username, password):
    if username not in db:
        raise KeyError('%s is not registered!' % username)
    else:
        if db[username] == get_md5(password + username + 'the-Salt'):
            print('%s login success.' % username)
        else:
            raise ValueError('%s\'s password is Wrong.' % username)


register('jim', '123456')
login('jim', '123456')
# login('jim','1234567')
# login('tom','123456')
# 摘要算法在很多地方都有广泛的应用。要注意摘要算法不是加密算法，不能用于加密（因为无法通过摘要反推明文），只能用于防篡改，但是它的单向计算特性决定了可以在不存储明文口令的情况下验证用户口令。

# itertools
# Python的内建模块itertools提供了非常有用的用于操作迭代对象的函数。
# 首先，我们看看itertools提供的几个“无限”迭代器
import itertools

natuals = itertools.count(1)
# for n in natuals:
#     print(n)
# 因为count()会创建一个无限的迭代器，所以上述代码会打印出自然数序列，根本停不下来，只能按Ctrl+C退出。
# cycle()会把传入的一个序列无限重复下去：
cs = itertools.cycle('ABCD')  # 注意字符串也是序列的一种
# for c in cs:
#     print(c)
# 同样停不下来。
# repeat()负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数：
ns = itertools.repeat('A', 3)
for n in ns:
    print(n)

# 无限序列只有在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来，事实上也不可能在内存中创建无限多个元素。
# 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列：
natuals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, natuals)
print(list(ns))
# itertools提供的几个迭代器操作函数更加有用：
# chain()
# chain()可以把一组迭代对象串联起来，形成一个更大的迭代器
for c in itertools.chain('ABC', 'XYZ'):
    print(c)

# groupby()
# groupby()把迭代器中相邻的重复元素挑出来放在一起
for key, group in itertools.groupby('AAABBBCCAAA'):
    print(key, list(group))

# 实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，
# 这两个元素就被认为是在一组的，而函数返回值作为组的key。如果我们要忽略大小写分组，就可以让元素'A'和'a'都返回相同的key
for key, group in itertools.groupby('AaAbbBccaaA', lambda c: c.upper()):
    print(key, list(group))
# itertools模块提供的全部是处理迭代功能的函数，它们的返回值不是list，而是Iterator，只有用for循环迭代的时候才真正计算。

# contextlib
# 在Python中，读写文件这样的资源要特别注意，必须在使用完毕后正确关闭它们。正确关闭文件资源的一个方法是使用try...finally：
try:
    f = open('README.md', 'r')
    print(f.readline())
finally:
    if f:
        f.close()
# 写try...finally非常繁琐。Python的with语句允许我们非常方便地使用资源，而不必担心资源没有关闭，所以上面的代码可以简化为：
with open('README.md', 'r') as f:
    print(f.readline())


# 并不是只有open()函数返回的fp对象才能使用with语句。实际上，任何对象，只要正确实现了上下文管理，就可以用于with语句。
# 实现上下文管理是通过__enter__和__exit__这两个方法实现的。例如，下面的class实现了这两个方法：
class Query(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)


# 这样我们就可以把自己写的资源对象用于with语句：
with Query('Bob') as q:
    q.query()

# @contextmanager
# 编写__enter__和__exit__仍然很繁琐，因此Python的标准库contextlib提供了更简单的写法，上面的代码可以改写如下：
from contextlib import contextmanager


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s.' % self.name)


@contextmanager
def create_query(name):
    print('Begin')
    q = Query(name)
    yield q
    print('End')


# @contextmanager这个decorator接受一个generator，
# 用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了：
with create_query('Jack') as q:
    q.query()


# 很多时候，我们希望在某段代码执行前后自动执行特定代码，也可以用@contextmanager实现。例如：
@contextmanager
def tag(name):
    print('<%s>' % name)
    yield
    print('</%s>' % name)


with tag('h1'):
    print('Hello')
    print('World')
# 代码的执行顺序是：
# with语句首先执行yield之前的语句，因此打印出<h1>；
# yield调用会执行with语句内部的所有语句，因此打印出hello和world；
# 最后执行yield之后的语句，打印出</h1>。
# 因此，@contextmanager让我们通过编写generator来简化上下文管理。
# @closing
# 如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象。例如，用with语句使用urlopen()：
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)
# closing也是一个经过@contextmanager装饰的generator，这个generator编写起来其实非常简单
# @contextmanager
# def closing(thing):
#     try:
#         yield thing
#     finally:
#         thing.close()
# 它的作用就是把任意对象变为上下文对象，并支持with语句。
# @contextlib还有一些其他decorator，便于我们编写更简洁的代码。

# XML
# XML虽然比JSON复杂，在Web中应用也不如以前多了，不过仍有很多地方在用，所以，有必要了解如何操作XML。
# DOM vs SAX
# 操作XML有两种方法：DOM和SAX。DOM会把整个XML读入内存，解析为树，因此占用内存大，解析慢，优点是可以任意遍历树的节点。SAX是流模式，边读边解析，占用内存小，解析快，缺点是我们需要自己处理事件。
# 正常情况下，优先考虑SAX，因为DOM实在太占内存。
# 在Python中使用SAX解析XML非常简洁，通常我们关心的事件是start_element，end_element和char_data，准备好这3个函数，然后就可以解析xml了。
# 举个例子，当SAX解析器读到一个节点时：

# <a href="/">python</a>

# 会产生3个事件：
# start_element事件，在读取<a href="/">时；
# char_data事件，在读取python时；
# end_element事件，在读取</a>时。

# 用代码实验一下：
from xml.parsers.expat import ParserCreate


class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('sax: start element: %s, attrs: %s' % (name, attrs))

    def end_element(self, name):
        print('sax: end element: %s' % name)

    def char_data(self, text):
        print('sax: char data: %s' % text)


xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)
# 需要注意的是读取一大段字符串时，CharacterDataHandler可能被多次调用，所以需要自己保存起来，在EndElementHandler里面再合并。
# 除了解析XML外，如何生成XML呢？99%的情况下需要生成的XML结构都是非常简单的，因此，最简单也是最有效的生成XML的方法是拼接字符串：
# L = []
# L.append(r'<?xml version="1.0"?>')
# L.append(r'<root>')
# L.append(encode('some & data'))
# L.append(r'</root>')
# return ''.join(L)
# 如果要生成复杂的XML呢？建议你不要用XML，改成JSON。
# 小结
# 解析XML时，注意找出自己感兴趣的节点，响应事件时，把节点数据保存起来。解析完毕后，就可以处理数据。

data = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
    <channel>
        <title>Yahoo! Weather - Beijing, CN</title>
        <lastBuildDate>Wed, 27 May 2015 11:00 am CST</lastBuildDate>
        <yweather:location city="Beijing" region="" country="China"/>
        <yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/>
        <yweather:wind chill="28" direction="180" speed="14.48" />
        <yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" />
        <yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/>
        <item>
            <geo:lat>39.91</geo:lat>
            <geo:long>116.39</geo:long>
            <pubDate>Wed, 27 May 2015 11:00 am CST</pubDate>
            <yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" />
            <yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" />
            <yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" />
            <yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" />
            <yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" />
            <yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" />
        </item>
    </channel>
</rss>
'''
from xml.parsers.expat import ParserCreate


class WeatherSaxHandler(object):
    def __init__(self):
        self._dict = {}
        self._forecast = []

    @property
    def dict(self):
        return self._dict

    # @property
    # def forecast(self):
    #     return self._forecast

    def start_element(self, name, attrs):
        print('start: (%s):(%s)' % (name, attrs))
        if name == 'yweather:location':
            self._dict.update(attrs)
        if name == 'yweather:forecast':
            self._forecast.append(attrs)

    def end_element(self, name):
        print('end: (%s)' % name)
        if name == 'rss':
            self._dict['today'] = self._forecast[0]
            self._dict['tomorrow'] = self._forecast[1]

    def char_data(self, text):
        print('char_data: %s' % text)
        pass


def parse_weather(xml):
    handler = WeatherSaxHandler()
    parser = ParserCreate()
    print('parser:', parser)
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)
    print('location', handler.dict)
    return handler.dict


weather = parse_weather(data)
assert weather['city'] == 'Beijing', weather['city']
assert weather['country'] == 'China', weather['country']
assert weather['today']['text'] == 'Partly Cloudy', weather['today']['text']
assert weather['today']['low'] == '20', weather['today']['low']
assert weather['today']['high'] == '33', weather['today']['high']
assert weather['tomorrow']['text'] == 'Sunny', weather['tomorrow']['text']
assert weather['tomorrow']['low'] == '21', weather['tomorrow']['low']
assert weather['tomorrow']['high'] == '34', weather['tomorrow']['high']
print('Weather:', str(weather))
