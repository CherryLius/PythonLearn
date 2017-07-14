# HTMLParser
# 如果我们要编写一个搜索引擎，第一步是用爬虫把目标网站的页面抓下来，第二步就是解析该HTML页面，看看里面的内容到底是新闻、图片还是视频。
# 假设第一步已经完成了，第二步应该如何解析HTML呢？
# HTML本质上是XML的子集，但是HTML的语法没有XML那么严格，所以不能用标准的DOM或SAX来解析HTML。
# 好在Python提供了HTMLParser来非常方便地解析HTML，只需简单几行代码：
from html.parser import HTMLParser
from html.entities import name2codepoint


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        name = chr(name2codepoint[name])
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href="#">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')

# feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去。
# 特殊字符有两种，一种是英文表示的&nbsp;，一种是数字表示的&#1234;，这两种字符都可以通过Parser解析出来
# 小结
# 利用HTMLParser，可以把网页中的文本、图像等解析出来。

# 找一个网页，例如https://www.python.org/events/python-events/，用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
from html.parser import HTMLParser
import re


class Event(object):
    def __init__(self, title, datetime, location):
        self.title = title
        self.datetime = datetime
        self.location = location


class EventHTMLParser(HTMLParser):
    def __init__(self):
        super(EventHTMLParser, self).__init__()
        self._events = []
        self._dict = {}

    @property
    def events(self):
        return self._events

    def handle_starttag(self, tag, attrs):
        print('start: (%s):(%s)' % (tag, attrs))
        if len(attrs) <= 0:
            return
        if tag == 'h3' and 'event-title' in attrs[0]:
            self._dict['title'] = 1
        if tag == 'time' and 'datetime' in attrs[0]:
            self._dict['time'] = 1
        if tag == 'span' and 'event-location' in attrs[0]:
            self._dict['location'] = 1

    def handle_endtag(self, tag):
        print('end: %s' % tag)
        if tag == 'li':
            e = Event(self._title, self._time, self._location)
            self._events.append(e)

    def handle_startendtag(self, tag, attrs):
        print('startendtag: (%s):(%s)' % (tag, attrs))

    def handle_comment(self, data):
        print('comment: %s' % data)

    def handle_entityref(self, name):
        print('entityref: %s' % name)

    def handle_charref(self, name):
        print('charref: %s' % name)

    def handle_data(self, data):
        print('data: %s' % data)
        if 'title' in self._dict and self._dict['title']:
            self._title = data
            self._dict['title'] = 0
        if 'time' in self._dict and self._dict['time']:
            self._time = data
            self._dict['time'] = 0
        if 'location' in self._dict and self._dict['location']:
            self._location = data
            self._dict['location'] = 0


def parse_html():
    parser = EventHTMLParser()
    with open('www.python.org.html', 'r') as f:
        html = ''.join(f.readlines())
        re_html = re.compile(r'<ul class="list-recent-events menu">([\s\S]*?)</ul>')
        all_event = re_html.findall(html)
        for event in all_event:
            parser.feed(event)
        print(parser.events)
        for event in parser.events:
            print('title:(%s), datetime=(%s), location=(%s).' % (event.title, event.datetime, event.location))


parse_html()

# urllib
# urllib提供了一系列用于操作URL的功能。

# Get
# urllib的request模块可以非常方便地抓取URL内容，也就是发送一个GET请求到指定的页面，然后返回HTTP的响应：
# 例如，对豆瓣的一个URL https://api.douban.com/v2/book/2129650进行抓取，并返回响应：
from urllib import request

with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s : %s' % (k, v))
    print('Data:', data.decode('utf-8'))
# 可以看到HTTP响应的头和JSON数据：
# 如果我们要想模拟浏览器发送GET请求，就需要使用Request对象，通过往Request对象添加HTTP头，我们就可以把请求伪装成浏览器。例如，模拟iPhone 6去请求豆瓣首页：
from urllib import request

req = request.Request('http://www.douban.com/')
req.add_header('User-Agent',
               'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s : %s' % (k, v))
    print('Data: ', f.read().decode('utf-8'))

# 这样豆瓣会返回适合iPhone的移动版网页：
# ...
#     <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0">
#     <meta name="format-detection" content="telephone=no">
#     <link rel="apple-touch-icon" sizes="57x57" href="http://img4.douban.com/pics/cardkit/launcher/57.png" />
# ...
# Post
# 如果要以POST发送一个请求，只需要把参数data以bytes形式传入。
# 我们模拟一个微博登录，先读取登录的邮箱和口令，然后按照weibo.cn的登录页的格式以username=xxx&password=xxx的编码传入：

# from urllib import request, parse
#
# print('Login to weibo.cn...')
# email = input('Email: ')
# password = input('Password: ')
# login_data = parse.urlencode([
#     ('username', email),
#     ('password', password),
#     ('entry', 'mweibo'),
#     ('client_id', ''),
#     ('savestate', '1'),
#     ('ec', ''),
#     ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
# ])
# req = request.Request('https://passport.weibo.cn/sso/login')
# req.add_header('Origin', 'https://passport.weibo.cn')
# req.add_header('User-Agent',
#                'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# req.add_header('Referer',
#                'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')
# with request.urlopen(req, data=login_data.encode('utf-8')) as f:
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s : %s' % (k, v))
#     print('Data:', f.read().decode('utf-8'))
# 如果登录成功，我们获得的响应如下：
# Status: 200 OK
# Server: nginx/1.2.0
# ...
# Set-Cookie: SSOLoginState=1432620126; path=/; domain=weibo.cn
# ...
# Data: {"retcode":20000000,"msg":"","data":{...,"uid":"1658384301"}}
# 如果登录失败，我们获得的响应如下：
#
# ...
# Data: {"retcode":50011015,"msg":"\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef","data":{"username":"example@python.org","errline":536}}
# Handler
#
# 如果还需要更复杂的控制，比如通过一个Proxy去访问网站，我们需要利用ProxyHandler来处理，示例代码如下：
# proxy_handler = request.ProxyHandler({'http': 'http://www.example.com:3128/'})
# proxy_auth_handler = request.ProxyBasicAuthHandler()
# proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
# opener = request.build_opener(proxy_handler, proxy_auth_handler)
# with opener.open('http://www.example.com/login.html') as f:
#     pass
# 小结
# urllib提供的功能就是利用程序去执行各种HTTP请求。如果要模拟浏览器完成特定功能，需要把请求伪装成浏览器。
# 伪装的方法是先监控浏览器发出的请求，再根据浏览器的请求头来伪装，User-Agent头就是用来标识浏览器的。
from urllib import request, parse
from xml.parsers.expat import ParserCreate


class WeatherSaxHandler(object):
    def __init__(self):
        self._dict = {}
        self._forecast = []

    @property
    def dict(self):
        return self._dict

    def start_element(self, name, attrs):
        print('Start: (%s) : (%s)' % (name, attrs))
        if name == 'yweather:location':
            self._dict.update(attrs)
        if name == 'yweather:forecast':
            self._forecast.append(attrs)

    def end_element(self, name):
        print('End: %s' % name)
        if name == 'query':
            self._dict['today'] = self._forecast[0]
            self._dict['tomorrow'] = self._forecast[1]

    def char_data(self, text):
        print('data: %s' % text)


def get_yahoo_weather(city):
    base_url = 'https://query.yahooapis.com/v1/public/yql?'
    yql_select = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % city
    yql_url = base_url + parse.urlencode([('q', yql_select)])
    with request.urlopen(yql_url) as f:
        print('Status:', f.status, f.reason)
        weather = f.read().decode('utf-8')
        print(weather)
        return weather


def fetch(city):
    weather = get_yahoo_weather(city)
    parser = ParserCreate()
    handler = WeatherSaxHandler()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(weather)
    print(handler.dict)


fetch('shanghai')
