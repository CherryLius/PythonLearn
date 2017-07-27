import asyncio

from webapp.www.models import User
from webapp.www.orm import create_pool


def test(loop):
    yield from create_pool(loop, user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    yield from u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
