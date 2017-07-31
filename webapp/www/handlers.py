' url handlers '
import asyncio, time
from webapp.www.coroweb import get, post
from webapp.www.models import User, Blog


@get('/')
@asyncio.coroutine
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200),
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
    # users = yield from User.findAll()
    # return {
    #     '__template__': 'test.html',
    #     'users': users
    # }


@get('/api/users')
@asyncio.coroutine
def api_get_users():
    users = yield from User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)
