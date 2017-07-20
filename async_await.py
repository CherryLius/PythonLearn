# async/await
# 用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。
#
# 为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。
#
# 请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
#
# 把@asyncio.coroutine替换为async；
# 把yield from替换为await。
# 让我们对比一下上一节的代码：
# import asyncio
#
#
# async def hello():
#     print('Hello world!')
#     r = await asyncio.sleep(1)
#     print('Hello Again!')
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()
# 小结
# Python从3.5版本开始为asyncio提供了async和await的新语法；
#
# 注意新语法只能用在Python 3.5以及后续版本，如果使用3.4版本，则仍需使用上一节的方案。
import asyncio


async def wGet(host):
    print('wGet: %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'Get / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    print('%s wirte header..' % host)
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


loop = asyncio.get_event_loop()
tasks = [wGet(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
