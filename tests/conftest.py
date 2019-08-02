import pytest
import asyncio
import random
import motor.motor_asyncio

from aiohttp.test_utils import loop_context

from polls.main_api_app.main import create_app
from polls.models.orm_models import Profile, Product
from polls.models.fake_model_manager import FakeModelManager
from polls.models.db import client
from tests.sub_functions import gen_vk_url
from polls.main_api_app.settings import APP_SECRET, COOKIE_NAME

from polls.main_api_app.elastick_client import ElastickClient

test_es_path = 'http://0.0.0.0:9200/test/product/'
TESTDATABASE = 'test_database'
fm = FakeModelManager()

@pytest.fixture(scope='session')
def loop():
    with loop_context() as _loop:
        yield _loop

@pytest.fixture(scope='session')
def event_loop(loop):
    yield loop

@pytest.fixture(scope='session')
def app(event_loop):
    global test_es_path

    yield create_app(loop=event_loop, dbname=TESTDATABASE, es_path=test_es_path)

@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client

@pytest.fixture
async def new_product_mongo(event_loop, app):
    product = await fm._create_fake_product()
    yield product
    await product.delete()

@pytest.fixture
async def new_10_products_mongo(event_loop, app):
    _ids = []
    for _ in range(10):
        product = await fm._create_fake_product()
        _ids.append(product._id)

    yield

    for _idx in _ids:
        await Product.objects.delete(_id=_idx)

@pytest.fixture
async def valid_cookie(event_loop, app, cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    yield cookie_data

    await Profile.objects.delete(vk_id=vk_id)

@pytest.fixture
async def new_product_in_app(event_loop, app):
    pattern = 'pattern'

    es_client = ElastickClient(path=test_es_path, loop=event_loop)
    es_client.connect()

    product = await fm._create_fake_product()
    product.product_name =  product.product_name + " " + pattern
    await product.save()

    await es_client.add_product(product)

    yield pattern

    await product.delete()
    # TODO удалять продукты из es

@pytest.fixture
async def new_profile_cookie_and_wish_id(event_loop, app, cli, valid_cookie, new_product_mongo):
    await cli.post('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : new_product_mongo._id})

    yield valid_cookie, new_product_mongo._id

@pytest.fixture
async def new_profile_and_cookie(event_loop, app, cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    prof = await Profile.objects.get(vk_id=vk_id)

    yield prof, cookie_data

    await Profile.objects.delete(vk_id=vk_id)

@pytest.fixture
async def profile_vkid_with_wish_and_prod_id(event_loop, app, cli, new_profile_and_cookie, new_product_mongo):
    profile, cookie = new_profile_and_cookie

    await cli.post('/profile/mypage/wishes', cookies=cookie, json={
        'product_id' : new_product_mongo._id})

    yield profile['vk_id'], new_product_mongo._id



