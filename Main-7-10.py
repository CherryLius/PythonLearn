# ThreadLocal
# 在多线程环境下，每个线程都有自己的数据。一个线程使用自己的局部变量比使用全局变量好，因为局部变量只有线程自己能看见，不会影响其他线程，而全局变量的修改必须加锁。
# 但是局部变量也有问题，就是在函数调用的时候，传递起来很麻烦
class Student(object):
    def __init__(self, name):
        self.name = name


# def process_student(name):
#     std = Student(name)
#     do_task_1(std)
#     do_task_2(std)
#
# def do_task_1(std):
#     do_subtask_1(std)
#     do_subtask_2(std)
#
# def do_task_2(std):
#     do_subtask_2(std)
#     do_subtask_2(std)
# 每个函数一层一层调用都这么传参数那还得了？用全局变量？也不行，因为每个线程处理不同的Student对象，不能共享。
# 如果用一个全局dict存放所有的Student对象，然后以thread自身作为key获得线程对应的Student对象如何？
#
# global_dict = {}
#
# def std_thread(name):
#     std = Student(name)
#     # 把std放到全局变量global_dict中：
#     global_dict[threading.current_thread()] = std
#     do_task_1()
#     do_task_2()
#
# def do_task_1():
#     # 不传入std，而是根据当前线程查找：
#     std = global_dict[threading.current_thread()]
#     ...
#
# def do_task_2():
#     # 任何函数都可以查找出当前线程的std变量：
#     std = global_dict[threading.current_thread()]
#     ...
# 这种方式理论上是可行的，它最大的优点是消除了std对象在每层函数中的传递问题，但是，每个函数获取std的代码有点丑。
# 有没有更简单的方式？
# ThreadLocal应运而生，不用查找dict，ThreadLocal帮你自动做这件事
import threading

# # 创建全局ThreadLocal对象:
local_school = threading.local()


def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
# 全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，但互不影响。
# 你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。
# 可以理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定其他变量，如local_school.teacher等等。
# ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源

# 小结
# 一个ThreadLocal变量虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题

# 分布式进程
# 在Thread和Process中，应当优选Process，因为Process更稳定，而且，Process可以分布到多台机器上，而Thread最多只能分布到同一台机器的多个CPU上

# Python的multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上。
# 一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。
# 由于managers模块封装很好，不必了解网络通信的细节，就可以很容易地编写分布式多进程程序

# 举个例子：如果我们已经有一个通过Queue通信的多进程程序在同一台机器上运行，现在，由于处理任务的进程任务繁重，
# 希望把发送任务的进程和处理任务的进程分布到两台机器上。怎么用分布式进程实现？
# 原有的Queue可以继续使用，但是，通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue了。
# 我们先看服务进程，服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写入任务
# task_master.py

# 请注意，当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，
# 但是，在分布式多进程环境下，添加任务到Queue不可以直接对原始的task_queue进行操作，
# 那样就绕过了QueueManager的封装，必须通过manager.get_task_queue()获得的Queue接口添加。
# 然后，在另一台机器上启动任务进程（本机上启动也可以）
# task_worker.py

# 这个简单的Master/Worker模型有什么用？其实这就是一个简单但真正的分布式计算，把代码稍加改造，
# 启动多个worker，就可以把任务分布到几台甚至几十台机器上，比如把计算n*n的代码换成发送邮件，就实现了邮件队列的异步发送。
# Queue对象存储在哪？注意到task_worker.py中根本没有创建Queue的代码，所以，Queue对象存储在task_master.py进程中

# 而Queue之所以能通过网络访问，就是通过QueueManager实现的。由于QueueManager管理的不止一个Queue，所以，要给每个Queue的网络调用接口起个名字，比如get_task_queue。
# authkey有什么用？这是为了保证两台机器正常通信，不被其他机器恶意干扰。如果task_worker.py的authkey和task_master.py的authkey不一致，肯定连接不上

# 小结
#
# Python的分布式进程接口简单，封装良好，适合需要把繁重任务分布到多台机器的环境下。
# 注意Queue的作用是用来传递任务和接收结果，每个任务的描述数据量要尽量小。
# 比如发送一个处理日志文件的任务，就不要发送几百兆的日志文件本身，而是发送日志文件存放的完整路径，由Worker进程再去共享的磁盘上读取文件。


# 正则表达式
# 正则表达式是一种用来匹配字符串的强有力的武器。
# 它的设计思想是用一种描述性的语言来给字符串定义一个规则，凡是符合规则的字符串，我们就认为它“匹配”了，否则，该字符串就是不合法的
# 所以我们判断一个字符串是否是合法的Email的方法是：
#   创建一个匹配Email的正则表达式；
#   用该正则表达式去匹配用户的输入来判断是否合法。
#
# 因为正则表达式也是用字符串表示的，所以，我们要首先了解如何用字符来描述字符。
#
# 在正则表达式中，如果直接给出字符，就是精确匹配。用\d可以匹配一个数字，\w可以匹配一个字母或数字，所以：
#
# '00\d'可以匹配'007'，但无法匹配'00A'；
#
# '\d\d\d'可以匹配'010'；
#
# '\w\w\d'可以匹配'py3'；
#
# .可以匹配任意字符，所以
# 'py.'可以匹配'pyc'、'pyo'、'py!'等等。

# 要匹配变长的字符，在正则表达式中，用*表示任意个字符（包括0个），用+表示至少一个字符，用?表示0个或1个字符，用{n}表示n个字符，用{n,m}表示n-m个字符：
# 来看一个复杂的例子：\d{3}\s+\d{3,8}。
# 我们来从左到右解读一下：
#   \d{3}表示匹配3个数字，例如'010'；
#   \s可以匹配一个空格（也包括Tab等空白符），所以\s+表示至少有一个空格，例如匹配' '，' '等；
#   \d{3,8}表示3-8个数字，例如'1234567'。
# 综合起来，上面的正则表达式可以匹配以任意个空格隔开的带区号的电话号码。
# 如果要匹配'010-12345'这样的号码呢？由于'-'是特殊字符，在正则表达式中，要用'\'转义，所以，上面的正则是\d{3}\-\d{3,8}。
# 但是，仍然无法匹配'010 - 12345'，因为带有空格。所以我们需要更复杂的匹配方式

# 进阶
# 要做更精确地匹配，可以用[]表示范围，比如：
#
# [0-9a-zA-Z\_]可以匹配一个数字、字母或者下划线；
#
# [0-9a-zA-Z\_]+可以匹配至少由一个数字、字母或者下划线组成的字符串，比如'a100'，'0_Z'，'Py3000'等等；
#
# [a-zA-Z\_][0-9a-zA-Z\_]*可以匹配由字母或下划线开头，后接任意个由一个数字、字母或者下划线组成的字符串，也就是Python合法的变量；
#
# [a-zA-Z\_][0-9a-zA-Z\_]{0, 19}更精确地限制了变量的长度是1-20个字符（前面1个字符+后面最多19个字符）。
#
# A|B可以匹配A或B，所以(P|p)ython可以匹配'Python'或者'python'。
#
# ^表示行的开头，^\d表示必须以数字开头。
#
# $表示行的结束，\d$表示必须以数字结束。
#
# 你可能注意到了，py也可以匹配'python'，但是加上^py$就变成了整行匹配，就只能匹配'py'了。

# re模块
# 有了准备知识，我们就可以在Python中使用正则表达式了。Python提供re模块，包含所有正则表达式的功能。由于Python的字符串本身也用\转义，所以要特别注意：
s = 'ABC\\-001'
# 对应的正则表达式字符串变成：
# 'ABC\-001'
# 因此我们强烈建议使用Python的r前缀，就不用考虑转义的问题了：
s = r'ABC\-001'
# 对应的正则表达式字符串不变：
# 'ABC\-001'

# 先看看如何判断正则表达式是否匹配：
import re

print(re.match(r'\d{3}\-\d{3,8}$', '010-123456'))
print(re.match(r'\d{3}\-\d{3,8}$', '010 123456'))
# match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。常见的判断方法就是
test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')

# 切分字符串
# 用正则表达式切分字符串比用固定的字符更灵活，请看正常的切分代码：
print('a b  c'.split(' '))
print(re.split(r'\s+', 'a b  c'))
print(re.split(r'[\s,]+', 'a, b,  c  d'))
# 再加入;试试：
print(re.split(r'[\s,;]+', 'a,b;; c  d'))

# 分组
# 除了简单地判断是否匹配之外，正则表达式还有提取子串的强大功能。用()表示的就是要提取的分组（Group）。比如
# ^(\d{3})-(\d{3,8})$分别定义了两个组，可以直接从匹配的字符串中提取出区号和本地号码
m = re.match(r'^(\d{3})-(\d{3,8})', '010-123456')
print(m.group(0))
print(m.group(1))
print(m.group(2))
# 如果正则表达式中定义了组，就可以在Match对象上用group()方法提取出子串来。
# 注意到group(0)永远是原始字符串，group(1)、group(2)……表示第1、2、……个子串
# 提取子串非常有用。来看一个更凶残的例子：
t = '19:05:30'
m = re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$', t)
print(m.groups())
# 贪婪匹配
# 最后需要特别指出的是，正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符。举例如下，匹配出数字后面的0：
print(re.match(r'^(\d+)(0*)$', '102300').groups())
# 由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了。
# 必须让\d+采用非贪婪匹配（也就是尽可能少匹配），才能把后面的0匹配出来，加个?就可以让\d+采用非贪婪匹配：
print(re.match(r'^(\d+?)(0*)$', '102300').groups())

# 编译
# 当我们在Python中使用正则表达式时，re模块内部会干两件事情：
# 编译正则表达式，如果正则表达式的字符串本身不合法，会报错；
# 用编译后的正则表达式去匹配字符串。
# 如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，
# 接下来重复使用时就不需要编译这个步骤了，直接匹配
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
print(re_telephone.match('010-1234567').groups())
print(re_telephone.match('010-8086').groups())

email_1 = 'someone@gmail.com'
email_2 = 'bill.gates@microsoft.com'
re_email = re.compile(r'^(\w+.?\w+)@(\w+).(\w+)$')
print(re_email.match(email_1))
print(re_email.match(email_2))
print(re_email.match(email_1).groups())
print(re_email.match(email_2).groups())
s = '<Tom Paris> tom@voyager.org'
m = re.compile(r'^(<.+>)\s+(\w+.?\w+@\w+.\w+)$')
print(m.match(s).groups())

# datetime
# 获取当前日期和时间
# 我们先看如何获取当前日期和时间
from datetime import datetime

now = datetime.now()
print(now)
print(type(now))
# 注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类。
# 如果仅导入import datetime，则必须引用全名datetime.datetime。
# datetime.now()返回当前日期和时间，其类型是datetime。

# 获取指定日期和时间
# 要指定某个日期和时间，我们直接用参数构造一个datetime
dt = datetime(2015, 4, 19, 12, 20)
print(dt)
# datetime转换为timestamp
# 在计算机中，时间实际上是用数字表示的。
# 我们把1970年1月1日 00:00:00 UTC+00:00时区的时刻称为epoch time，
# 记为0（1970年以前的时间timestamp为负数），当前时间就是相对于epoch time的秒数，称为timestamp。
# 你可以认为：
# timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00
# 对应的北京时间是：
# timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00
# 可见timestamp的值与时区毫无关系，因为timestamp一旦确定，其UTC时间就确定了，
# 转换到任意时区的时间也是完全确定的，这就是为什么计算机存储的当前时间是以timestamp表示的，
# 因为全球各地的计算机在任意时刻的timestamp都是完全相同的（假定时间已校准）。
# 把一个datetime类型转换为timestamp只需要简单调用timestamp()方法
print(dt.timestamp())
# 注意Python的timestamp是一个浮点数。如果有小数位，小数位表示毫秒数。
# 某些编程语言（如Java和JavaScript）的timestamp使用整数表示毫秒数，
# 这种情况下只需要把timestamp除以1000就得到Python的浮点表示方法

# timestamp转换为datetime
# 要把timestamp转换为datetime，使用datetime提供的fromtimestamp()方法：
t = 1429417200.0
print(datetime.fromtimestamp(t))

# 注意到timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的。上述转换是在timestamp和本地时间做转换。
# 本地时间是指当前操作系统设定的时区。例如北京时区是东8区，则本地时间：
# 2015-04-19 12:20:00
# 实际上就是UTC+8:00时区的时间：
# 2015-04-19 12:20:00 UTC+8:00
# 而此刻的格林威治标准时间与北京时间差了8小时，也就是UTC+0:00时区的时间应该是：
# 2015-04-19 04:20:00 UTC+0:00
# timestamp也可以直接被转换到UTC标准时区的时间：
print(datetime.utcfromtimestamp(t))

# str转换为datetime
# 很多时候，用户输入的日期和时间是字符串，要处理日期和时间，
# 首先必须把str转换为datetime。转换方法是通过datetime.strptime()实现，需要一个日期和时间的格式化字符串
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)

# 字符串'%Y-%m-%d %H:%M:%S'规定了日期和时间部分的格式。详细的说明请参考Python文档。
# 注意转换后的datetime是没有时区信息的
# datetime转换为str
# 如果已经有了datetime对象，要把它格式化为字符串显示给用户，就需要转换为str，转换方法是通过strftime()实现的，同样需要一个日期和时间的格式化字符串
now = datetime.now()
print(now.strftime('%Y-%m-%d %H:%M:%S'))
