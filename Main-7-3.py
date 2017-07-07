# 迭代器
#
# 可以直接作用于for循环的数据类型有以下几种：
# 一类是集合数据类型，如list、tuple、dict、set、str等；
# 一类是generator，包括生成器和带yield的generator function。
# 这些可以直接作用于for循环的对象统称为可迭代对象：Iterable。
# 可以使用isinstance()判断一个对象是否是Iterable对象
from collections import Iterable

print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance((x for x in range(10)), Iterable))
print(isinstance(100, Iterable))

# 生成器不但可以作用于for循环，还可以被next()函数不断调用并返回下一个值，直到最后抛出StopIteration错误表示无法继续返回下一个值了。
# 可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
# 可以使用isinstance()判断一个对象是否是Iterator对象
from collections import Iterator

print(isinstance((x for x in range(10)), Iterator))
print(isinstance([], Iterator))
# 生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。
# 把list、dict、str等Iterable变成Iterator可以使用iter()函数：
print(isinstance(iter([]), Iterator))
# 你可能会问，为什么list、dict、str等数据类型不是Iterator？
# 这是因为Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。
# 可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，
# 所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
# Iterator甚至可以表示一个无限大的数据流，例如全体自然数。而使用list是永远不可能存储全体自然数的

#
# 凡是可作用于for循环的对象都是Iterable类型；
# 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
# 集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
# Python的for循环本质上就是通过不断调用next()函数实现的，例如:
for x in [1, 2, 3, 4, 5]:
    pass
# 实际上完全等价于：
# 首先获得Iterator对象
it = iter([1, 2, 3, 4, 5])
# 循环
while True:
    try:
        # 获得下一个值
        x = next(it)
    except StopIteration:
        # 捕获异常退出
        break

# 函数式编程
# 高阶函数
# 函数名也是变量
f = abs
print(f(-10))


# 既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数
def add(x, y, f):
    return f(x) + f(y)


print(add(-10, 5, abs))


# map/reduce
# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def f(x):
    return x ** 2


r = map(f, [1, 2, 3, 4, 5, 6])
print(list(r))
# map()传入的第一个参数是f，即函数对象本身。由于结果r是一个Iterator，Iterator是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list
print(list(map(str, [1, 2, 3, 4, 5, 6])))

# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
# 对序列求和
from functools import reduce


def add(x, y):
    return x + y


print(reduce(add, [1, 2, 3, 4]))


# 当然求和运算可以直接用Python内建函数sum()，没必要动用reduce。
# 但是如果要把序列[1, 3, 5, 7, 9]变换成整数13579，reduce就可以派上用场
def fn(x, y):
    return x * 10 + y


print(reduce(fn, [1, 3, 5, 7, 9]))


def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]


print(reduce(fn, map(char2num, '135790')))


# 整理成一个str2int的函数就是
def str2int(s):
    def fn(x, y):
        return x * 10 + y

    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

    return reduce(fn, map(char2num, s))


print(str2int('0123456'))


# 用lambda函数进一步简化成
def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))


print(str2int('56789'))


#
def normalize(name):
    return name.capitalize()


L1 = ['adam', 'LISA', 'barT']
print(list(map(normalize, L1)))


def prod(L):
    return reduce(lambda x, y: x * y, L)


print(prod([3, 5, 7, 9]))


def str2float(s):
    if '.' in s:
        index = s.index('.')
        l = len(s)
        n = l - index - 1
        return reduce(lambda x, y: 10 * x + y, map(char2num, s[:index])) + (
            reduce(lambda x, y: x * 10 + y, map(char2num, s[index + 1:l])) / (10 ** n))
    else:
        return reduce(lambda x, y: 10 * x + y, map(char2num, s))


print('str2float(\'123.456\') =', str2float('123.456'))
print(str2float('123'))


# filter
# Python内建的filter()函数用于过滤序列。
# 和map()类似，filter()也接收一个函数和一个序列。
# 和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
def is_odd(n):
    return n % 2 == 1


print(list(filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9])))


# 把一个序列中的空字符串删掉，可以这么写
def not_empty(s):
    return s and s.strip()


print(list(filter(not_empty, ['A', 'B', None, '', 'C', ' ', 'D '])))


def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


for n in primes():
    if n < 1000:
        print(n)
    else:
        break


# 回数
def is_palindrome(n):
    s = str(n)
    return s == s[::-1]


print(list(filter(is_palindrome, range(1, 10000))))

# 排序算法
# Python内置的sorted()函数就可以对list进行排序
print(sorted([36, 5, -12, 9, -21]))
# sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序
print(sorted([36, 5, - 12, 9, - 21], key=abs))
# 字符串排序
print(sorted(['bob', 'about', 'Zoo', 'Credit']))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]


def by_name(t):
    return t[0]


def by_score(t):
    return t[1]


print(sorted(L, key=by_name))
print(sorted(L, key=by_score, reverse=True))


# 返回函数
# 在这个例子中，我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
# 当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。
# 请再注意一点，当我们调用lazy_sum()时，每次调用都会返回一个新的函数，即使传入相同的参数
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax

    return sum


f = lazy_sum(1, 3, 5, 7, 9)
f2 = lazy_sum(1, 3, 5, 7, 9)
print(f)
print(f())
print(f == f2)


# 闭包
# 注意到返回的函数在其定义内部引用了局部变量args，
# 所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。
# 另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了f()才执行。我们来看一个例子
def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


f1, f2, f3 = count()
print(f1())
print(f2())
print(f3())


# 全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。
# 返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。
# 如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变
def count():
    def f(j):
        def g():
            return j * j

        return g

    fs = []
    for i in range(1, 4):
        fs.append(f(i))
    return fs


f1, f2, f3 = count()
print(f1())
print(f2())
print(f3())
# 一个函数可以返回一个计算结果，也可以返回一个函数。
# 返回一个函数时，牢记该函数并未执行，返回函数中不要引用任何可能会变化的变量


# 匿名函数
# 当我们在传入函数时，有些时候，不需要显式地定义函数，直接传入匿名函数更方便。
# 在Python中，对匿名函数提供了有限支持。还是以map()函数为例，计算f(x)=x2时，除了定义一个f(x)的函数外，还可以直接传入匿名函数
print(list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])))
# 关键字lambda表示匿名函数，冒号前面的x表示函数参数
# 匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
# 用匿名函数有个好处，因为函数没有名字，不必担心函数名冲突。
# 此外，匿名函数也是一个函数对象，也可以把匿名函数赋值给一个变量，再利用变量来调用该函数：
f = lambda x: x * x
print(f, f(5))


# 同样，也可以把匿名函数作为返回值返回
def build(x, y):
    return lambda: x * x + y * y


print(build(3, 4)())


# 装饰器
def now():
    print('2017-7-3')


f = now
f()
# 函数对象有一个__name__属性，可以拿到函数的名字
print(now.__name__)
print(f.__name__)


# 现在，假设我们要增强now()函数的功能，比如，在函数调用前后自动打印日志，但又不希望修改now()函数的定义，
# 这种在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）。
# 本质上，decorator就是一个返回函数的高阶函数。所以，我们要定义一个能打印日志的decorator，可以定义如下
def log(func):
    def wrapper(*args, **kw):
        print('call %s()' % func.__name__)
        return func(*args, **kw)

    return wrapper


# 观察上面的log，因为它是一个decorator，所以接受一个函数作为参数，并返回一个函数。
# 我们要借助Python的@语法，把decorator置于函数的定义处
@log
def now():
    print('2017-7-3')


# 调用now()函数，不仅会运行now()函数本身，还会在运行now()函数前打印一行日志
# 把@log放到now()函数的定义处，相当于执行了语句：
# now = log(now)
now()


# 由于log()是一个decorator，返回一个函数，所以，原来的now()函数仍然存在，只是现在同名的now变量指向了新的函数，
# 于是调用now()将执行新函数，即在log()函数中返回的wrapper()函数。
#
# wrapper()函数的参数定义是(*args, **kw)，因此，wrapper()函数可以接受任意参数的调用。在wrapper()函数内，首先打印日志，再紧接着调用原始函数。
#
# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s()' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log('execute')
def now():
    print('2017-7-3')


# now = log('execute')(now)
now()
# 我们来剖析上面的语句，首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。
# 以上两种decorator的定义都没有问题，但还差最后一步。因为我们讲了函数也是对象，它有__name__等属性，
# 但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper'
print(now.__name__)
# 因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
# 不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下
import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('%s()' % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
def now():
    print('2017-7-3')


print(now.__name__)


def log(text):
    def decorator(func=text):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s() begin call' % (text, func.__name__))
            _func = func(*args, **kw)
            print('%s %s() end call' % (text, func.__name__))
            return _func

        return wrapper
    return decorator(text) if hasattr(text, '__call__') else decorator


@log(1111)
def f():
    print('call method print')


@log
def f2():
    print('call method print 2')


f()
f2()

# 偏函数
# Python的functools模块提供了很多有用的功能，其中一个就是偏函数（Partial function）
# int()函数可以把字符串转换为整数，当仅传入字符串时，int()函数默认按十进制转换：
#
# >>> int('12345')
# 12345
# 但int()函数还提供额外的base参数，默认值为10。如果传入base参数，就可以做N进制的转换
print(int('12345', base=8))
print(int('12345', base=16))


def int2(x, base=2):
    return int(x, base)


print(int2('1000000'))
print(int2('1010101'))
# functools.partial就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接使用下面的代码创建一个新的函数int2
import functools

int2 = functools.partial(int, base=2)
print(int2('1000000'))
print(int2('1010101'))
# functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单
print(int2('1000000', base=10))
# 创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数，当传入
# int2 = functools.partial(int, base=2)
# 实际上固定了int()函数的关键字参数base，也就是：
#
# int2('10010')
# 相当于：
# kw = { 'base': 2 }
# int('10010', **kw)
# 当传入：
# max2 = functools.partial(max, 10)
# 实际上会把10作为*args的一部分自动加到左边，也就是：
# max2(5, 6, 7)
# 相当于：
# args = (10, 5, 6, 7)
# max(*args)
# 结果为10。
max2 = functools.partial(max, 10)
print(max2(5, 6, 7))
# 当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。

# ***********************************************
'a test module'
__author__ = 'Test'
import sys


def test():
    args = sys.argv
    if len(args) == 1:
        print('Hello World!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')


if __name__ == '__main__':
    test()


# 第1行和第2行是标准注释，第1行注释可以让这个hello.py文件直接在Unix/Linux/Mac上运行，第2行注释表示.py文件本身使用标准UTF-8编码；
#
# 第4行是一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释；
#
# 第6行使用__author__变量把作者写进去，这样当你公开源代码后别人就可以瞻仰你的大名；
#
# 以上就是Python模块的标准文件模板，当然也可以全部删掉不写，但是，按标准办事肯定没错。
#
# 后面开始就是真正的代码部分。
#
# 你可能注意到了，使用sys模块的第一步，就是导入该模块：

# 最后，注意到这两行代码：
#
# if __name__=='__main__':
#     test()
# 当我们在命令行运行hello模块文件时，Python解释器把一个特殊变量__name__置为__main__，
# 而如果在其他地方导入该hello模块时，if判断将失败，因此，这种if测试可以让一个模块通过命令行运行时执行一些额外的代码，最常见的就是运行测试。
# ************************************************

# 作用域

# 在一个模块中，我们可能会定义很多函数和变量，但有的函数和变量我们希望给别人使用，有的函数和变量我们希望仅仅在模块内部使用。在Python中，是通过_前缀来实现的。
# 正常的函数和变量名是公开的（public），可以被直接引用，比如：abc，x123，PI等；
# 类似__xxx__这样的变量是特殊变量，可以被直接引用，但是有特殊用途，比如上面的__author__，__name__就是特殊变量，
# hello模块定义的文档注释也可以用特殊变量__doc__访问，我们自己的变量一般不要用这种变量名；
# 类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等；
# 之所以我们说，private函数和变量“不应该”被直接引用，而不是“不能”被直接引用，是因为Python并没有一种方法可以完全限制访问private函数或变量，
# 但是，从编程习惯上不应该引用private函数或变量。
# private函数或变量不应该被别人引用，那它们有什么用呢？
def _private_1(name):
    return 'Hello, %s' % name


def _private_2(name):
    return 'Hi, %s' % name


def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)


# 我们在模块里公开greeting()函数，而把内部逻辑用private函数隐藏起来了，
# 这样，调用greeting()函数不用关心内部的private函数细节，这也是一种非常有用的代码封装和抽象的方法，即：
# 外部不需要引用的函数全部定义成private，只有外部需要引用的函数才定义为public

# Pillow
from PIL import Image

im = Image.open('test.png')
print(im.format, im.size, im.mode)

im.thumbnail((408, 325))
im.save('thumbnail.jpg', 'JPEG')
print('end')


# 面向对象
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s : %s' % (self.name, self.score))


bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.print_score()
lisa.print_score()


# class后面紧接着是类名，即Student，类名通常是大写开头的单词，紧接着是(object)，表示该类是从哪个类继承下来的，继承的概念我们后面再讲，
# 通常，如果没有合适的继承类，就使用object类，这是所有类最终都会继承的类
# 通过定义一个特殊的__init__方法，在创建实例的时候，就把name，score等属性绑上去

# class Student(object):
#     pass
#
#
# bart = Student()
# bart.name = 'Bart Simpson'
#
# print(bart.name)

# 可以自由地给一个实例变量绑定属性，比如，给实例bart绑定一个name属性
# 到__init__方法的第一个参数永远是self，表示创建的实例本身，因此，在__init__方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。
# 有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，但self不需要传，Python解释器自己会把实例变量传进去
# 普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数

# 数据封装
# 类的方法
# 如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，
# 在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问，所以，我们把Student类改一改
class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s : %s' % (self.__name, self.__score))


bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.print_score()
lisa.print_score()
# 在Python中，变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，
# 特殊变量是可以直接访问的，不是private变量，所以，不能用__name__、__score__这样的变量名

# 有些时候，你会看到以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，
# 当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。
# 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。
# 不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量
print(bart._Student__name)


# 继承和多态
class Animal(object):
    def run(self):
        print('Animal is Running')


class Dog(Animal):
    def eat(self):
        print('Dog is eating')

    def run(self):
        print('Dog is Running')


class Cat(Animal):
    def run(self):
        print('Cat is Running')


dog = Dog()
dog.run()
cat = Cat()
cat.run()

# 静态语言 vs 动态语言
#
# 对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。
#
# 对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了：
#
# class Timer(object):
#     def run(self):
#         print('Start...')
# 这就是动态语言的“鸭子类型”，它并不要求严格的继承体系，一个对象只要“看起来像鸭子，走起路来像鸭子”，那它就可以被看做是鸭子

# Python的“file-like object“就是一种鸭子类型。对真正的文件对象，它有一个read()方法，返回其内容.
# 但是，许多对象，只要有read()方法，都被视为“file-like object“。
# 许多函数接收的参数就是“file-like object“，你不一定要传入真正的文件对象，完全可以传入任何实现了read()方法的对象。


# 获取对象信息
# 当我们拿到一个对象的引用时，如何知道这个对象是什么类型、有哪些方法呢？
# 使用type()
# 首先，我们来判断对象类型，使用type()函数：
# 基本类型都可以用type()判断：
print(type(123))
print(type('abc'))
print(type(None))
print(type(abs))
print(type(dog))
# 判断基本数据类型可以直接写int，str等，但如果要判断一个对象是否是函数怎么办？可以使用types模块中定义的常量：
import types


def fn():
    pass


print(type(fn) == types.FunctionType)
print(type(abs) == types.BuiltinFunctionType)
print(type(lambda x: x * x) == types.LambdaType)
print(type((x for x in range(10))) == types.GeneratorType)

# 使用isinstance()

isinstance(123, int)
isinstance(dog, Dog)
isinstance(dog, Animal)
# 还可以判断一个变量是否是某些类型中的一种:
isinstance([1, 2, 3], (list, tuple))
isinstance((1, 2, 3), (list, tuple))

# 使用dir()

# 如果要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list，比如，获得一个str对象的所有属性和方法
print(dir('ABC'))


# 类似__xxx__的属性和方法在Python中都是有特殊用途的，比如__len__方法返回长度。
# 在Python中，如果你调用len()函数试图获取一个对象的长度，实际上，在len()函数内部，它自动去调用该对象的__len__()方法，所以，下面的代码是等价的：

# >>> len('ABC')
# 3
# >>> 'ABC'.__len__()
# 3
# 我们自己写的类，如果也想用len(myObj)的话，就自己写一个__len__()方法
class MyObject(object):
    def __len__(self):
        return 100


obj = MyObject()
print(len(obj))


# 仅把属性和方法列出来是不够的，配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态
class MyObject(object):
    def __init__(self):
        self.x = 9

    def power(self):
        return self.x * self.x

    def __len__(self):
        return 10


obj = MyObject()
print(len(obj))
print(hasattr(obj, 'x'))  # 有属性'x'吗？
print(hasattr(obj, 'y'))
setattr(obj, 'y', 19)  # 设置一个属性'y'
print(hasattr(obj, 'y'))
print(getattr(obj, 'y'))  # 获取属性'y'
print(obj.y)
# 如果试图获取不存在的属性，会抛出AttributeError的错误
# print(getattr(obj, 'z'))
# 可以传入一个default参数，如果属性不存在，就返回默认值：
print(getattr(obj, 'z', 100))
# 可以获得对象的方法
print(hasattr(obj, 'power'))
fn = getattr(obj, 'power')
print(fn())


# 实例属性和类属性
# 类属性 直接在class中定义属性，这种属性是类属性，归Student类所有
# 当我们定义了一个类属性后，这个属性虽然归类所有，但类的所有实例都可以访问到
class Student(object):
    name = 'Student'


s = Student()
print(s.name)
print(Student.name)
#  给实例绑定name属性
#  由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
s.name = 'Michael'
print(s.name)
# 但是类属性并未消失，用Student.name仍然可以访问
print(Student.name)
# 如果删除实例的name属性
# 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了
del s.name
print(s.name)


# 使用__slots__
# 正常情况下，当我们定义了一个class，创建了一个class的实例后，我们可以给该实例绑定任何属性和方法，这就是动态语言的灵活性
class Student(object):
    pass


# 尝试给实例绑定一个属性：
s = Student()
s.name = 'Micheal'
print(s.name)


# 可以尝试给实例绑定一个方法：
def set_age(self, age):
    self.age = age


from types import MethodType

s.set_age = MethodType(set_age, s)  # 给实例绑定一个方法
s.set_age(25)  # 调用实例方法
print(s.age)
# 但是，给一个实例绑定的方法，对另一个实例是不起作用的
s2 = Student()


# s2.set_age(18)
# 为了给所有实例都绑定方法，可以给class绑定方法
# 给class绑定方法后，所有实例均可调用
def set_score(self, score):
    self.score = score


Student.set_score = set_score

s.set_score(20)
print(s.score)
s2.set_score(50)
print(s2.score)


# 使用__slots__
# 但是，如果我们想要限制实例的属性怎么办？比如，只允许对Student实例添加name和age属性。
# 为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性
class Student(object):
    __slots__ = ('name', 'age')  # 用tuple定义允许绑定的属性名称


s = Student()
s.name = 'Micheal'
s.age = 40


# s.score = 10
# 用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
# 除非在子类中也定义__slots__，这样，子类实例允许定义的属性就是自身的__slots__加上父类的__slots__。
class GraduateStudent(Student):
    pass


g = GraduateStudent()
g.score = 60
print(g.score)
