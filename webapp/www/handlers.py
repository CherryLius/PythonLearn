' url handlers '
import asyncio
from webapp.www.coroweb import get, post
from webapp.www.models import User


@get('/')
@asyncio.coroutine
def index(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
