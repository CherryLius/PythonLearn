# datetime加减
# 对日期和时间进行加减实际上就是把datetime往后或往前计算，得到新的datetime。加减可以直接用+和-运算符，不过需要导入timedelta这个类
from datetime import datetime, timedelta

now = datetime.now()
print(now)

print(now + timedelta(hours=10))
print(now - timedelta(days=1))
print(now + timedelta(days=2, hours=12))
# 可见，使用timedelta你可以很容易地算出前几天和后几天的时刻。

# 本地时间转换为UTC时间
# 本地时间是指系统设定时区的时间，例如北京时间是UTC+8:00时区的时间，而UTC时间指UTC+0:00时区的时间
# 一个datetime类型有一个时区属性tzinfo，但是默认为None，所以无法区分这个datetime到底是哪个时区，除非强行给datetime设置一个时区
from datetime import datetime, timezone, timedelta

tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
now = datetime.now()
print(now)
dt = now.replace(tzinfo=tz_utc_8)
print(dt)
# 如果系统时区恰好是UTC+8:00，那么上述代码就是正确的，否则，不能强制设置为UTC+8:00时区。

# 时区转换
# 我们可以先通过utcnow()拿到当前的UTC时间，再转换为任意时区的时间

# # 拿到UTC时间，并强制设置时区为UTC+0:00:
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
# astimezone()将转换时区为北京时间:
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
# astimezone()将转换时区为东京时间:
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt)
# # astimezone()将bj_dt转换时区为东京时间:
dj_dt = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(dj_dt)

# 时区转换的关键在于，拿到一个datetime时，要获知其正确的时区，然后强制设置时区，作为基准时间。
# 利用带时区的datetime，通过astimezone()方法，可以转换到任意时区。
# 注：不是必须从UTC+0:00时区转换到其他时区，任何带时区的datetime都可以正确转换，例如上述bj_dt到tokyo_dt的转换

# 小结
# datetime表示的时间需要时区信息才能确定一个特定的时间，否则只能视为本地时间。
# 如果要存储datetime，最佳方法是将其转换为timestamp再存储，因为timestamp的值与时区完全无关。

import re
from datetime import datetime, timezone, timedelta


def to_timestamp(dt_str, tz_str):
    print('to_timestamp start...')
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    print(dt)
    m = re.match(r'^\w+(.\d+):0\d+?$', tz_str)
    hours = int(m.group(1))
    print(hours)
    utc_tz = timezone(timedelta(hours=hours))
    dt = dt.replace(tzinfo=utc_tz)
    print(re.split(r'[UTC:]+', tz_str))
    return dt.timestamp()


t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
print(t1)
assert t1 == 1433121030.0, t1
t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

# collections
# collections是Python内建的一个集合模块，提供了许多有用的集合类。
# namedtuple
# 我们知道tuple可以表示不变集合，例如，一个点的二维坐标就可以表示成
p = (1, 2)
# 但是，看到(1, 2)，很难看出这个tuple是用来表示一个坐标的。
# 定义一个class又小题大做了，这时，namedtuple就派上了用场
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)
# namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
# 这样一来，我们用namedtuple可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。
# 可以验证创建的Point对象是tuple的一种子类
print(isinstance(p, Point))
print(isinstance(p, tuple))
# 类似的，如果要用坐标和半径表示一个圆，也可以用namedtuple定义：
# # namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])

# deque

# 使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。
# deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈
from collections import deque

q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)
# deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素。

# defaultdict
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict

dd = defaultdict(lambda: 'N/A')
dd['k1'] = 'abc'
print(dd['k1'])
print(dd['k2'])
# 注意默认值是调用函数返回的，而函数在创建defaultdict对象时传入。
# 除了在Key不存在时返回默认值，defaultdict的其他行为跟dict是完全一样的

# OrderedDict

# 使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。
# 如果要保持Key的顺序，可以用OrderedDict：
from collections import OrderedDict

d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)  # dict的Key是无序的
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)
# OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：
od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3
print(od)
print(list(od.keys()))  # 按照插入的Key的顺序返回
# OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：
from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):
    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)


lod = LastUpdatedOrderedDict(2)
lod['a'] = 1
lod['b'] = 2
lod['c'] = 3
lod['c'] = 4
print(lod)

# Counter
# Counter是一个简单的计数器，例如，统计字符出现的个数：
from collections import Counter

c = Counter()
for ch in 'Programming':
    c[ch] = c[ch] + 1

print(c)
# Counter实际上也是dict的一个子类，上面的结果可以看出，字符'g'、'm'、'r'各出现了两次，其他字符各出现了一次。
# collections模块提供了一些有用的集合类，可以根据需要选用。

# base64
# Base64是一种用64个字符来表示任意二进制数据的方法。
# 用记事本打开exe、jpg、pdf这些文件时，我们都会看到一大堆乱码，因为二进制文件包含很多无法显示和打印的字符，所以，如果要让记事本这样的文本处理软件能处理二进制数据，就需要一个二进制到字符串的转换方法。Base64是一种最常见的二进制编码方法。
# Base64的原理很简单，首先，准备一个包含64个字符的数组：
# ['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']
# 然后，对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit：
# 这样我们得到4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串。
# 所以，Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示。
# 如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉。
# Python内置的base64可以直接进行base64的编解码：
import base64

b = base64.b64encode(b'binary\x00string')
print(b)
b = base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
print(b)
# 由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_：
b = base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')
print(b)
b = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
print(b)
b = base64.urlsafe_b64decode('abcd--__')
print(b)


# 还可以自己定义64个字符的排列顺序，这样就可以自定义Base64编码，不过，通常情况下完全没有必要。
# Base64是一种通过查表的编码方法，不能用于加密，即使使用自定义的编码表也不行。
# Base64适用于小段内容的编码，比如数字证书签名、Cookie的内容等。
# 由于=字符也可能出现在Base64编码中，但=用在URL、Cookie里面会造成歧义，所以，很多Base64编码后会把=去掉：
# # 标准Base64:
# 'abcd' -> 'YWJjZA=='
# # 自动去掉=:
# 'abcd' -> 'YWJjZA'
# 去掉=后怎么解码呢？因为Base64是把3个字节变为4个字节，所以，Base64编码的长度永远是4的倍数，因此，需要加上=把Base64字符串的长度变为4的倍数，就可以正常解码了。
# Base64是一种任意二进制到文本字符串的编码方法，常用于在URL、Cookie、网页中传输少量二进制数据。
def safe_base64_decode(s):
    if isinstance(s, bytes):
        return base64.b64decode(s + b'=' * (4 - len(s) % 4))
    elif isinstance(s, str):
        return base64.b64decode(s + '=' * (4 - len(s) % 4))


print('safe base64 decode start...')
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('pass')

# struct
# 准确地讲，Python没有专门处理字节的数据类型。但由于b'str'可以表示字节，所以，字节数组＝二进制str。而在C语言中，我们可以很方便地用struct、union来处理字节，以及字节和int，float的转换。
# 在Python中，比方说要把一个32位无符号整数变成字节，也就是4个长度的bytes，你得配合位运算符这么写
# >> > n = 10240099
# >> > b1 = (n & 0xff000000) >> 24
# >> > b2 = (n & 0xff0000) >> 16
# >> > b3 = (n & 0xff00) >> 8
# >> > b4 = n & 0xff
# >> > bs = bytes([b1, b2, b3, b4])
# >> > bs
# b'\x00\x9c@c'
#
# 非常麻烦。如果换成浮点数就无能为力了。
# 好在Python提供了一个struct模块来解决bytes和其他二进制数据类型的转换。
# struct的pack函数把任意数据类型变成bytes：
import struct
b = struct.pack('>I', 10240099)
print(b)
# pack的第一个参数是处理指令，'>I'的意思是：
# >表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。
# 后面的参数个数要和处理指令一致。
# unpack把bytes变成相应的数据类型：
print(struct.unpack('>IH',b'\xf0\xf0\xf0\xf0\x80\x80'))
# 根据>IH的说明，后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数
# 所以，尽管Python不适合编写底层操作字节流的代码，但在对性能要求不高的地方，利用struct就方便多了。
# struct模块定义的数据类型可以参考Python官方文档：
# https://docs.python.org/3/library/struct.html#format-characters
# Windows的位图文件（.bmp）是一种非常简单的文件格式，我们来用struct分析一下。
# 首先找一个bmp文件，没有的话用“画图”画一个。
# 读入前30个字节来分析：
s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
# BMP格式采用小端方式存储数据，文件头的结构按顺序如下：
# 两个字节：'BM'表示Windows位图，'BA'表示OS/2位图；
# 一个4字节整数：表示位图大小；
# 一个4字节整数：保留位，始终为0；
# 一个4字节整数：实际图像的偏移量；
# 一个4字节整数：Header的字节数；
# 一个4字节整数：图像宽度；
# 一个4字节整数：图像高度；
# 一个2字节整数：始终为1；
# 一个2字节整数：颜色数。
# 所以，组合起来用unpack读取：
_struct = struct.unpack('<ccIIIIIIHH', s)
print(_struct)