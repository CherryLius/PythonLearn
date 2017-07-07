# 高级特性
# 切片
# 普通去list或tuple的部分元素的做法
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[0], L[1], L[2])

r = []
n = 3
for i in range(n):
    r.append(L[i])
print(r)
# 对这种经常取指定索引范围的操作，用循环十分繁琐，因此，Python提供了切片（Slice）操作符，能大大简化这种操作。
# 对应上面的问题，取前3个元素，用一行代码就可以完成切片：
print('Slice0:', L[0:3])
print('Slice1:', L[:3])
print('Slice2:', L[-2:])
print('Slice3:', L[-1:])
L = list(range(99))
print(L[:10])  # 前10个数
print(L[-10:])  # 后10个数
print(L[:10:2])  # 前10个数，每2个取1个
print(L[::5])  # 所有数，每5个取一个
print(L[:])  # 只写[:]就可以原样复制一个list
# 对于tuple的切片操作跟list相同
T = tuple(list(range(10)))
print(T[:3])
# 字符串'xxx'也可以看成是一种list，每个元素就是一个字符。因此，字符串也可以用切片操作，只是操作结果仍是字符串
print('Hello+World'[:3])
print('Hello+World'[::2])

# 迭代
# dict的迭代
d = {'a': 0, 'b': 1, 'c': 2}
for key in d:  # 迭代key
    print(key)
for val in d.values():  # 迭代value
    print(val)
# 同时迭代key和value
for K, V in d.items():
    print(K, V)
# 字符串迭代
for ch in 'HelloWorld':
    print(ch)
# 如何判断一个对象是可迭代对象呢？方法是通过collections模块的Iterable类型判断
from collections import Iterable

print(isinstance('abc', Iterable))
# 对list实现类似Java那样的下标循环怎么办？
# Python内置的enumerate函数可以把一个list变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身
for i, v in enumerate(['A', 'B', 'C']):
    print(i, v)

for x, y in [(1, 2), (3, 4), (5, 6)]:
    print(x, y)

# 列表生成式
# 列表生成式即List Comprehensions，是Python内置的非常简单却强大的可以用来创建list的生成式
print('List comprehensions')
L = [x * x for x in range(1, 11)]
print(L)
# for 循环后面还可以添加条件判断
L = [x * x for x in range(1, 11) if x % 2 == 0]
print(L)

S = [m + n for m in 'ABC' for n in 'XYZ']
print(S)
# 列出当前目录下所有文件和目录名
import os

D = [d for d in os.listdir('.')]
print(D)
d = {'a': 0, 'b': 1, 'c': 2}
L = [k + '=' + str(v) for k, v in d.items()]
print(L)

# 把一个list所有字符串变成小写
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])

L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]
print('L2:', L2)

# 生成器
# 通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。
# 而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，
# 如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。
#
# 所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？
# 这样就不必创建完整的list，从而节省大量的空间。
# 在Python中，这种一边循环一边计算的机制，称为生成器：generator

# 要创建一个generator，有很多种方法。第一种方法很简单，只要把一个列表生成式的[]改成()，就创建了一个generator
L = [x * x for x in range(10)]  # 列表生成式
print(L)

g = (x * x for x in range(10))  # 生成器
print(g)
# 通过next()函数获得generator的下一个返回值
print(next(g))
for n in g:
    print(n)


# 斐波那契数列 1, 1, 2, 3, 5, 8, 13, 21, 34,...
def fibonacci(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n += 1
    return 'done'


print(fibonacci(9))


# 仔细观察，可以看出，fib函数实际上是定义了斐波拉契数列的推算规则，可以从第一个元素开始，推算出后续任意的元素，这种逻辑其实非常类似generator。
# 也就是说，上面的函数和generator仅一步之遥。要把fib函数变成generator，只需要把print(b)改为yield b就可以了：
def fibonacci(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n += 1
    return 'done'


# 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator
f = fibonacci(9)
print(f)
for n in fibonacci(9):
    print(n)


# 函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
# 而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
def odd():
    print('Step1')
    yield 1
    print('Step2')
    yield 2
    print('Step3')
    yield 5


print('odd Start')
o = odd()
print(next(o))
print(next(o))
print(next(o))
print('odd End')


# 杨辉三角
#           1
#         1   1
#       1   2   1
#     1   3   3   1
#   1   4   6   4   1
# 1   5   10  10  5   1
def triangles():
    L = [1]
    while True:
        yield L
        L.append(0)
        L = [L[i - 1] + L[i] for i in range(len(L))]


n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break
