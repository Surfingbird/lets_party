import asyncio
import pytest
import random
import http

from tests.sub_functions import gen_vk_url
from polls.main_api_app.settings import APP_SECRET, COOKIE_NAME

async def test_auth_success(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    assert respose.status == 200

async def test_auth_fail(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    respose = await cli.post('/auth', json = {'url':url})
    assert respose.status == 401

async def test_auth_invali_request_another_data(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    respose = await cli.post('/auth', data='test_auth_invali_request_another_data')
    assert respose.status == 400

async def test_auth_invali_request_empty_data(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    respose = await cli.post('/auth')
    assert respose.status == 400

async def test_unauth_success(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    respose = await cli.post('/auth', json = {'url':url})
    cookie = respose.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    respose = await cli.delete('/auth', cookies={'value' : cookie.value})
    assert respose.status == 200


async def test_get_products(cli, new_product, valid_cookie):
    respose = await cli.get('/products', cookies=valid_cookie)

    data = await respose.json()

    assert type(data) == list
    for item in data:
        print(item)

    assert respose.status == 200