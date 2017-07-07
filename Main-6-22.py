# -*- coding: utf-8 -*-

# print("hello python")
# print input()
# name = input('please enter your name: \n')
# print('name=', name)
# 缩进代码遇到 : 表示代码块
a = 100
if a >= 100:
    print(a)
else:
    print(-a)
# Python允许用r''表示''内部的字符串默认不转义
print('\\t\\')
print(r'\\t\\')
# 字符串内部有很多换行，用\n写在一行里不好阅读，Python允许用'''...'''的格式表示多行内容
# 以上是在交互式命令行内输入，注意在输入多行内容时，提示符由>>>变为...，提示你可以接着上一行输入
print('line1\nline2\nline3')

print('''line1
...line2
...line3''')

print('''line1
line2
line3''')

print(r'''\line1
line2
line3''')
# 一个布尔值只有True、False两种值
# 在Python中，可以直接用True、False表示布尔值（请注意大小写）
# 布尔值可以用and、or和not运算。
# and运算是与运算 or运算是或运算 not运算是非运算
# 对应java的 and-&&、or-||、not-!
print(3 > 2)
age = 17
if age >= 18:
    print("adult")
else:
    print("teenager")
# Python里一个特殊的值，用None表示。None不能理解为0，因为0是有意义的，而None是一个特殊的空值
# 动态变量 静态变量 类似groovy
# 动态
a = 123
print('a=', a)
a = 'A String'
print('a=', a)
# 静态
# int b = 123
# b = 'abc' # 错误
# Python中默认的编码格式是 ASCII 格式，在没修改编码格式时无法正确打印汉字，所以在读取中文时会报错。
# 解决方法为只要在文件开头加入 # -*- coding: UTF-8 -*- 或者 #coding=utf-8
# 在 Python 里，标识符有字母、数字、下划线组成。
# 在 Python 中，所有标识符可以包括英文、数字以及下划线(_)，但不能以数字开头。
# Python 中的标识符是区分大小写的。
# 以下划线开头的标识符是有特殊意义的。以单下划线开头 _foo 的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 from xxx import * 而导入；
# 以双下划线开头的 __foo 代表类的私有成员；以双下划线开头和结尾的 __foo__ 代表 Python 里特殊方法专用的标识，如 __init__() 代表类的构造函数。
# Python 可以同一行显示多条语句，方法是用分号 ; 分开

# Python 保留字符
# and	exec	not
# assert	finally	or
# break	for	pass
# class	from	print
# continue	global	raise
# def	if	return
# del	import	try
# elif	in	while
# else	is	with
# except	lambda	yield

# 对于单个字符的编码，Python提供了ord()函数获取字符的整数表示，chr()函数把编码转换为对应的字符
print(ord('A'))
print(ord('中'))
print(chr(66))
print(chr(25991))
print('\u4e2d\u6587')

# 由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
# 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes。
# Python对bytes类型的数据用带b前缀的单引号或双引号表示
x = b'ABC'
print(x)
# 以Unicode表示的str通过encode()方法可以编码为指定的bytes
print('ABC'.encode('ascii'))
print('中文'.encode('utf-8'))
# 从网络或磁盘上读取了字节流，那么读到的数据就是bytes。要把bytes变为str，就需要用decode()方法
print(b'ABC'.decode('ascii'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))
# str包含多少个字符，可以用len()函数
print(len('ABC'))
print(len(b'\xe4\xb8\xad\xe6\x96\x87'))
# 格式化
# %运算符就是用来格式化字符串的。在字符串内部，%s表示用字符串替换，%d表示用整数替换，
# 有几个%?占位符，后面就跟几个变量或者值，顺序要对应好。如果只有一个%?，括号可以省略。
#
# 常见的占位符有：
#
# %d	整数
# %f	浮点数
# %s	字符串
# %x	十六进制整数
print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Micheal', 1000))
print('%2d-%02d' % (3, 1))
print('%.2f' % 3.0)
print('growth rate %d%%' % 7)
# list
classmates = ['Michael', 'Bob', "Tracy"]
print(len(classmates))
print(classmates[0])
# 追加
classmates.append('David')
print(classmates)
# 插入
classmates.insert(1, 'Jack')
print(classmates)
# 删除
# classmates.pop()
classmates.pop(1)
print(classmates)
# list中不同元素
L = ['Apple', 123, True]
print(L)
# 元素可以是另一个元素
s = ['Python', 'Java', ['Asp', 'Php'], 'Scheme']
print(s)

# uple
# 另一种有序列表叫元组：tuple。
# tuple和list非常类似，但是tuple一旦初始化就不能修改
# 当你定义一个tuple时，在定义的时候，tuple的元素就必须被确定下来
classmates = ('Michael', 'Bob', 'Tracy')
print(classmates)
# 定义一个只有1个元素的tuple
t = (1,)
print(t)
classmates = ('Michael', "Bob", ['Jack', 'David'])
classmates[2][1] = 'Rose'
classmates[2].append('Tom')
print(classmates)
# 条件判断
age = 20
if age >= 18:
    print('your age is', age)
    print('Adult')
elif age >= 6:
    print('your age is', age)
    print('Teenager')
else:
    print('your age is', age)
    print('Kid')

# if判断条件还可以简写，比如写：
# if x:
#     print('True')
# 只要x是非零数值、非空字符串、非空list等，就判断为True，否则为False。
# s = input('birth:\n')
# # input()返回结果是str
# birth = int(s)
# if birth > 2000:
#     print('大于2000')
# else:
#     print('小于2000')

# 循环
# Python的循环有两种，一种是for...in循环，依次把list或tuple中的每个元素迭代出来
for name in classmates:
    print(name)
sum = 0
for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    sum += x
print('sum=', sum)
# range()函数，可以生成一个整数序列，再通过list()函数可以转换为list
l = list(range(5))
print(l)

sum = 0
for x in range(101):
    sum += x
print('sum=', sum)
# while循环
sum = 0
n = 99
while n > 0:
    sum += n
    n -= 2
print('while sum = %d' % sum)
n = 0
while n <= 100:
    n += 1
    if n > 10:
        break
    if n % 2 == 0:
        continue
    print(n)

print('While End')

# dict
# Python内置了字典：dict的支持，dict全称dictionary，
# 在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度
d = {'Michael': 95, 'Bob': 70, 'Tracy': 35}
print(d['Michael'])
d['Adam'] = 73
print(d)
d['Tracy'] = 60
print(d)
# 是否存在key xxx in d
print('Jim' in d)
# 通过dict提供的get方法，如果key不存在，可以返回None，或者自己指定的value
print(d.get('Bob'))
print(d.get('Jim'))
print(d.get('Jim', -1))
# 删除pop()键值对一起删除
d.pop('Bob')
print(d)

# Set
# set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
# 要创建一个set，需要提供一个list作为输入集合
s = set([1, 2, 3, 3, 5])
print(s)
# 添加
s.add(4)
# 删除
s.remove(5)
print(s)
# set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)

a = ['c', 'b', 'a']
print(a)
a.sort()
print(a)
a = 'abc'
print(a)
print(a.replace('a', 'A'))
print(a)

# 不带list的tuple可以作为key
# 带list的tuple不行，无法判断是否同一个key
t = ('a', 'b', 'c')
# t = ('a', 'b', 'c', ['d', 'e'])
d = {'k1': 123, 'k2': 321, t: 1}
print(d)

# 函数
print(abs(123))
print(max(1, 2, 3, 4, 5))
# 数据类型转换
print(int('123'))
print(int(12.34))
print(float('12.34'))
print(str(12.3))
print(bool(1))

print(bool(0))
print(bool(''))
# 函数名其实就是指向一个函数对象的引用，完全可以把函数名赋给一个变量，相当于给这个函数起了一个“别名”
a = abs
print(a(-1))


# 定义函数
# 定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:
# 在缩进块中编写函数体，函数的返回值用return语句返回
# return None简写return
# def my_abs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x
#
#
# print(my_abs(-10))


# 如果你已经把my_abs()的函数定义保存为abstest.py文件了，
# 可以在该文件的当前目录下启动Python解释器，
# 用from abstest import my_abs来导入my_abs()函数，注意abstest是文件名（不含.py扩展名）

# 空函数
# 定义一个什么事也不做的空函数，可以用pass语句
# pass可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个pass，让代码能运行起来
def nop():
    pass


# pass还可以用在其他语句里，比如：
# 缺少了pass，代码运行就会有语法错误。
# if age >= 18:
#     pass

# 参数类型检查
# 数据类型检查可以用内置函数isinstance()实现
# raise 抛出异常
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


print(my_abs(-1))
# 返回值 多个值: 返回tuple

import math


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny


print(move(100, 100, 60, math.pi / 6))


def quadratic(a, b, c):
    f = math.sqrt(b ** 2 - 4 * a * c)
    x1 = (-b + f) / (2 * a)
    x2 = (-b - f) / (2 * a)
    return x1, x2


print(quadratic(2, 3, 1))
print(quadratic(1, 3, -4))


# 函数参数 x^2 x^3
# 默认参数
def power(x, n=2):
    s = 1
    while n > 0:
        n -= 1
        s *= x
    return s


print(power(3))
print(power(3, 3))
