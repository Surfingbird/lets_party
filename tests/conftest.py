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

# TODO FIX BUG WITH DELETE PRODUCT
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
    print('cookie id ', vk_id)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    yield cookie_data

    await Profile.objects.delete(vk_id=vk_id)

@pytest.fixture
async def cookie_with_profile_dict(event_loop, app, cli):
    vk_id = random.randint(1, 1000000000)
    print('cookie id ', vk_id)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    profile = await Profile.objects.get(vk_id=vk_id)

    yield cookie_data, profile

    await Profile.objects.delete(vk_id=vk_id)

@pytest.fixture
async def second_cookie_with_profile_dict(event_loop, app, cli):
    vk_id = random.randint(1, 1000000000)
    print('cookie id ', vk_id)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    profile = await Profile.objects.get(vk_id=vk_id)

    yield cookie_data, profile

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

@pytest.fixture
async def cookie_with_intention(event_loop, app, cli, valid_cookie, profile_vkid_with_wish_and_prod_id):
    dest_id, product_id = profile_vkid_with_wish_and_prod_id

    res = await cli.post('/profile/mypage/intentions', cookies=valid_cookie, json={
        'product_id' : product_id,
        'dest_id' : dest_id})
    assert res.status == 201

    yield valid_cookie

@pytest.fixture
async def cookie_pid_destid_prof_with_wish(event_loop, app, cli, valid_cookie, profile_vkid_with_wish_and_prod_id):
    dest_id, product_id = profile_vkid_with_wish_and_prod_id

    res = await cli.post('/profile/mypage/intentions', cookies=valid_cookie, json={
        'product_id' : product_id,
        'dest_id' : dest_id})
    assert res.status == 201

    yield valid_cookie, product_id, dest_id

@pytest.fixture
async def profile_with_wish_and_product(event_loop, app, cli, new_product_mongo):
    vk_id = random.randint(1, 1000000000)
    print('vk_id wont ', vk_id)
    prof = Profile(vk_id=vk_id)
    await prof.save()

    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    dest_cookie = respose.cookies[COOKIE_NAME]
    dest_cookie_data = {'value' : dest_cookie.value}

    res = await cli.post('/profile/mypage/wishes', cookies=dest_cookie_data,
    json={'product_id' : new_product_mongo._id})
    assert res.status == 201

    yield prof, new_product_mongo

    await prof.delete()

@pytest.fixture
async def profile_with_reserved_wish(event_loop, app, cli, profile_with_wish_and_product):
    sponsor_vk_id = random.randint(1, 1000000000)
    print('vk_id sponsor ', sponsor_vk_id)
    sponsor_prof = Profile(vk_id=sponsor_vk_id)
    await sponsor_prof.save()

    sponsor_url = gen_vk_url(sponsor_vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':sponsor_url})
    sponsor_cookie = respose.cookies[COOKIE_NAME]
    sponsor_cookie_data = {'value' : sponsor_cookie.value}

    dest_prof, product = profile_with_wish_and_product

    res = await cli.post('/profile/mypage/intentions',
    cookies=sponsor_cookie_data, 
    json={
        'product_id' : product._id,
        'dest_id' : dest_prof.vk_id
    })
    assert res.status == 201

    yield dest_prof

    await sponsor_prof.delete()

@pytest.fixture
async def cookie_and_profile_with_res_intention(event_loop, app, cli, valid_cookie, profile_with_wish_and_product):
    dest_prof, product = profile_with_wish_and_product

    res = await cli.post('/profile/mypage/intentions',
    cookies=valid_cookie, 
    json={
        'product_id' : product._id,
        'dest_id' : dest_prof.vk_id
    })
    assert res.status == 201

    yield valid_cookie, dest_prof