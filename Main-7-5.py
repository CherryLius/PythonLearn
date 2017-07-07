# 错误处理
# 高级语言通常都内置了一套try...except...finally...的错误处理机制
try:
    print('try...')
    # r = 10 / int('a')
    r = 10 / 0
    r = 10 / 2
    print('result=', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('except:', e)
else:
    print('No Error')
finally:
    print('finally...')
print('End...')
# 当我们认为某些代码可能会出错时，就可以用try来运行这段代码，
# 如果执行出错，则后续代码不会继续执行，而是直接跳转至错误处理代码，
# 即except语句块，执行完except后，如果有finally语句块，则执行finally语句块，至此，执行完毕
# 如果发生了不同类型的错误，应该由不同的except语句块处理。没错，可以有多个except来捕获不同类型的错误：
# 如果没有错误发生，可以在except语句块后面加一个else，当没有错误发生时，会自动执行else语句
# Python的错误其实也是class，所有的错误类型都继承自BaseException，
# 所以在使用except时需要注意的是，它不但捕获该类型的错误，还把其子类也“一网打尽”
# 使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，比如函数main()调用foo()，foo()调用bar()，结果bar()出错了，这时，只要main()捕获到了
# 不需要在每个可能出错的地方去捕获错误，只要在合适的层次去捕获错误就可以了。这样一来，就大大减少了写try...except...finally的麻烦

# 调用堆栈
# 如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息，然后程序退出

# 记录错误
# 如果不捕获错误，自然可以让Python解释器来打印出错误堆栈，但程序也被结束了。既然我们能捕获错误，就可以把错误堆栈打印出来，然后分析错误原因，同时，让程序继续执行下去。
# Python内置的logging模块可以非常容易地记录错误信息
import logging


def foo(s):
    return 0 / int(s)


def bar(s):
    return foo(s) * 2


def main():
    try:
        bar(0)
    except Exception as e:
        logging.exception(e)


main()
print('End')


# 通过配置，logging还可以把错误记录到日志文件里，方便事后排查。

# 抛出异常
# 因为错误是class，捕获一个错误就是捕获到该class的一个实例。因此，错误并不是凭空产生的，而是有意创建并抛出的。Python的内置函数会抛出很多类型的错误，我们自己编写的函数也可以抛出错误。
# 如果要抛出错误，首先根据需要，可以定义一个错误的class，选择好继承关系，然后，用raise语句抛出一个错误的实例
class FooError(ValueError):
    pass


def foo(s):
    n = int(s)
    if n == 0:
        raise FooError('invalid value: %s' % s)
    return 10 / n


# foo('0')
def bar():
    try:
        foo('0')
    except FooError as e:
        print('FooError', e)
        raise


# bar()
# raise语句如果不带参数，就会把当前错误原样抛出。此外，在except中raise一个Error，还可以把一种类型的错误转化成另一种类型
# try:
#     10 / 0
# except ZeroDivisionError:
#     raise ValueError('input error!')
# 只要是合理的转换逻辑就可以，但是，决不应该把一个IOError转换成毫不相干的ValueError

# 调试
# 第一种方法简单直接粗暴有效，就是用print()把可能有问题的变量打印出来看看
# 用print()最大的坏处是将来还得删掉它，想想程序里到处都是print()，运行结果也会包含很多垃圾信息。所以，我们又有第二种方法
# 断言
# 凡是用print()来辅助查看的地方，都可以用断言（assert）来替代
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero'
    return 10 / n


def main():
    foo('1')


main()


# assert的意思是，表达式n != 0应该是True，否则，根据程序运行的逻辑，后面的代码肯定会出错
# 如果断言失败，assert语句本身就会抛出AssertionError
# 程序中如果到处充斥着assert，和print()相比也好不到哪去。不过，启动Python解释器时可以用-O参数来关闭assert
# 关闭后，你可以把所有的assert语句当成pass来看

# logging
# 把print()替换为logging是第3种方式，和assert比，logging不会抛出错误，而且可以输出到文件
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
# print('Logging')
# s = '0'
# n = int(s)
# logging.info('n = %d' % n)
# print(10 / n)
# logging.info()就可以输出一段文本。运行，发现除了ZeroDivisionError，没有任何信息。怎么回事？
# 别急，在import logging之后添加一行配置再试试
# import logging
# logging.basicConfig(level=logging.INFO)

# 这就是logging的好处，它允许你指定记录信息的级别，有debug，info，warning，error等几个级别，
# 当我们指定level=INFO时，logging.debug就不起作用了。同理，指定level=WARNING后，debug和info就不起作用了。
# 这样一来，你可以放心地输出不同级别的信息，也不用删除，最后统一控制输出哪个级别的信息。
# logging的另一个好处是通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件。


# pdb
# 第4种方式是启动Python的调试器pdb，让程序以单步方式运行，可以随时查看运行状态。我们先准备好程序

# # err.py
# s = '0'
# n = int(s)
# print(10 / n)

# 然后启动：

# $ python3 -m pdb err.py
# > /Users/michael/Github/learn-python3/samples/debug/err.py(2)<module>()
# -> s = '0'

# 以参数-m pdb启动后，pdb定位到下一步要执行的代码-> s = '0'。输入命令l来查看代码

# 输入命令n可以单步执行代码：
#
# (Pdb) n
# > /Users/michael/Github/learn-python3/samples/debug/err.py(3)<module>()
# -> n = int(s)
# (Pdb) n
# > /Users/michael/Github/learn-python3/samples/debug/err.py(4)<module>()
# -> print(10 / n)

# 任何时候都可以输入命令p 变量名来查看变量：
#
# (Pdb) p s
# '0'
# (Pdb) p n
# 0
# 输入命令q结束调试，退出程序：
#
# (Pdb) q
# 这种通过pdb在命令行调试的方法理论上是万能的，但实在是太麻烦了
# 我们还有另一种调试方法

# pdb.set_trace()
# 这个方法也是用pdb，但是不需要单步执行，我们只需要import pdb，然后，在可能出错的地方放一个pdb.set_trace()，就可以设置一个断点

# import pdb
#
# s = '0'
# n = int(s)
# pdb.set_trace()  # 运行到这里会自动暂停
# print(10 / n)

# 运行代码，程序会自动在pdb.set_trace()暂停并进入pdb调试环境，可以用命令p查看变量，或者用命令c继续运行：


# IDE
# 如果要比较爽地设置断点、单步执行，就需要一个支持调试功能的IDE。目前比较好的Python IDE有PyCharm：
# http://www.jetbrains.com/pycharm/
# 另外，Eclipse加上pydev插件也可以调试Python程序。
# 小结
# 写程序最痛苦的事情莫过于调试，程序往往会以你意想不到的流程来运行，你期待执行的语句其实根本没有执行，这时候，就需要调试了。
# 虽然用IDE调试起来比较方便，但是最后你会发现，logging才是终极武器

# 单元测试
# mydict.py mydict_test.py

# 编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。
# 以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。
# 对每一类测试都需要编写一个test_xxx()方法。
# 由于unittest.TestCase提供了很多内置的条件判断，我们只需要调用这些方法就可以断言输出是否是我们所期望的。
# 最常用的断言就是assertEqual()
# self.assertEqual(abs(-1), 1) # 断言函数返回的结果与1相等

# 另一种重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError
# with self.assertRaises(KeyError):
#     value = d['empty']

# 而通过d.empty访问不存在的key时，我们期待抛出AttributeError：
# with self.assertRaises(AttributeError):
#     value = d.empty

# 运行单元测试
#
# 一旦编写好单元测试，我们就可以运行单元测试。最简单的运行方式是在mydict_test.py的最后加上两行代码：
#
# if __name__ == '__main__':
#     unittest.main()
# 这样就可以把mydict_test.py当做正常的python脚本运行：
#
# $ python3 mydict_test.py
# 另一种方法是在命令行通过参数-m unittest直接运行单元测试：
#
# $ python3 -m unittest mydict_test
# .....
# ----------------------------------------------------------------------
# Ran 5 tests in 0.000s
#
# OK
# 这是推荐的做法，因为这样可以一次批量运行很多单元测试，并且，有很多工具可以自动来运行这些单元测试

# setUp与tearDown
# 可以在单元测试中编写两个特殊的setUp()和tearDown()方法。这两个方法会分别在每调用一个测试方法的前后分别被执行。
# setUp()和tearDown()方法有什么用呢？
# 设想你的测试需要启动一个数据库，这时，就可以在setUp()方法中连接数据库，在tearDown()方法中关闭数据库，这样，不必在每个测试方法中重复相同的代码：


# 文档测试

# 如果你经常阅读Python的官方文档，可以看到很多文档都有示例代码。比如re模块就带了很多示例代码：
#
# >>> import re
# >>> m = re.search('(?<=abc)def', 'abcdef')
# >>> m.group(0)
# 'def'
# 可以把这些示例代码在Python的交互式环境下输入并执行，结果与文档中的示例代码显示的一致。
#
# 这些代码与其他说明可以写在注释中，然后，由一些工具来自动生成文档。既然这些代码本身就可以粘贴出来直接运行，那么，可不可以自动执行写在注释中的这些代码呢？
#
# 答案是肯定的。
# 当我们编写注释时，如果写上这样的注释：
def abs(n):
    '''
    Function to get absolute value of number.

    Example:

    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''
    return n if n >= 0 else (-n)


# 无疑更明确地告诉函数的调用者该函数的期望输入和输出。
# 并且，Python内置的“文档测试”（doctest）模块可以直接提取注释中的代码并执行测试。
# doctest严格按照Python交互式命令行的输入和输出来判断测试结果是否正确。只有测试异常的时候，可以用...表示中间一大段烦人的输出。
# 让我们用doctest来测试上次编写的Dict类：

# 运行python3 mydict.py：
# $ python3 mydict.py
# 什么输出也没有。这说明我们编写的doctest运行都是正确的。如果程序有问题，比如把__getattr__()方法注释掉，再运行就会报错
# 注意到最后3行代码。当模块正常导入时，doctest不会被执行。只有在命令行直接运行时，才执行doctest。所以，不必担心doctest会在非测试环境下执行

def fact(n):
    '''
    >>> fact(0)
    Traceback (most recent call last):
        ...
    ValueError
    >>> fact(1)
    1
    >>> fact(2)
    2
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
