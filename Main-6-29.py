def enroll(name, gender):
    print('name=%s' % name)
    print('gender=%s' % gender)


enroll('Sarah', 'F')


def enroll(name, gender, age=6, city='Shanghai'):
    print('name=%s' % name)
    print('gender=%s' % gender)
    print('age=%d' % age)
    print('city=%s' % city)


enroll('Tom', 'M')
enroll('Bob', 'M', 8)
enroll('Jerry', 'M', city='TianJin')


# 默认参数的坑
# 定义默认参数要牢记一点：默认参数必须指向不变对象
# L=[]指定了可变的对象
def add_end(L=[]):
    L.append('END')
    return L


print(add_end([1, 2, 3]))
print(add_end())
print(add_end())


# 多次调用add_end()，默认参数列表内容会改变
# Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，
# 因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，
# 则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了
# 修改如下:
def add_end(L=None):
    if L is None:
        L = []
    L.append('End')
    return L


print(add_end())
print(add_end())


# 可变参数即不定长参数
# def calc(numbers):
#     sum = 0
#     for x in numbers:
#         sum += x * x
#     return sum
#
#
# print(calc([1, 2, 3, 4, 5]))


# 定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号。
# 在函数内部，参数numbers接收到的是一个tuple，因此，函数代码完全不变。
# 但是，调用该函数时，可以传入任意个参数，包括0个参数
def calc(*nums):
    ret = 0
    for n in nums:
        ret += n * n
    return ret


print(calc(4, 5, 6))
# 如果已经有一个list或者tuple，要调用一个可变参数怎么办
# Python允许你在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去
numbers = (1, 2, 3, 4)
print(calc(*numbers))


# 关键字参数
# 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
# 而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name=', name, 'age=', age, ',other=', kw)


person('Michael', 30)
person('Bob', 10, city='Shanghai')
person('Adam', '26', gender='M', city='Beijing')
# 和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', '32', **extra)


# **表示把extra这个dict的所有key-value用关键字参数传入到函数的**kw参数，
# kw将获得一个dict，注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra

# 命名关键字参数
# def person(name, age, **kw):
#     if 'city' in kw:
#         pass
#     if 'job' in kw:
#         pass
#     print(name, age, kw)
#
# person('Jack', 24, city='Beijing', addr='ChaoYang', zipcode=123456)
# 如果要限制关键字参数的名字，就可以用命名关键字参数，
# 例如，只接收city和job作为关键字参数。这种方式定义的函数如下
# 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)


person('Rose', '24', city='Shanghai', job='Waitress')


# 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
def person(name, age, *args, city, job):
    print(name, age, args, city, job)


person('ABD', 2, 1, 2, 3, city='ABC', job='XYZ')


# 命名关键字参数可以有缺省值
def person(name, age, *, city='Shanghai', job):
    print(name, age, city, job)


person('Jakie', 18, job='Stu')


# 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。
# 但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数

def f1(a, b, c=0, *args, **kw):
    print('f1: a=', a, ' b=', b, ' c=', c, ' args=', args, ' extra=', kw)


def f2(a, b, c=0, *, d, **kw):
    print('f2: a=', a, ' b=', b, ' c=', c, ' d=', d, ' kw=', kw)


f1(1, 2)
f1(1, 2, c=3)
f1(1, 2, 3, 'a', 'b')
f1(1, 2, 3, 'a', 'b', x=99)
f2(1, 2, d=99, ext=None)
# 最神奇的是通过一个tuple和dict，你也可以调用上述函数
args = (1, 2, 3, 4)
kw = {'d': 99, 'x': '#'}
f1(*args, **kw)
args = (1, 2, 3)
f2(*args, **kw)


# 递归函数
def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


print(fact(3))
print(fact(5))


# 解决递归调用栈溢出的方法是通过尾递归优化，
# 事实上尾递归和循环的效果是一样的，所以，把循环看成是一种特殊的尾递归函数也是可以的
# 尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。
# 这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况
# 上述尾递归写法：
def fact(n):
    return fact_iter(n, 1)


def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)


print(fact(5))

# 尾递归调用时，如果做了优化，栈不会增长，因此，无论多少次调用也不会导致栈溢出。
# 遗憾的是，大多数编程语言没有针对尾递归做优化，Python解释器也没有做优化，
# 所以，即使把上面的fact(n)函数改成尾递归方式，也会导致栈溢出。

# 汉诺塔经典算法
# 当A塔上有n个盘子是，先将A塔上编号1至n-1的盘子（共n-1个）移动到B塔上（借助C塔），
# 然后将A塔上最大的n号盘子移动到C塔上，最后将B塔上的n-1个盘子借助A塔移动到C塔上
step = 0


def move(n, _from, _to):
    global step
    step = step + 1
    print("第%d步，将第%d号盘子从%s---->%s" % (step, n, _from, _to))


def hanoi(n, _from, _depend, _to):
    if n == 1:
        move(1, _from, _to)
        return
    hanoi(n - 1, _from, _to, _depend)
    move(n, _from, _to)
    hanoi(n - 1, _depend, _from, _to)


hanoi(3, 'A', 'B', 'C')
