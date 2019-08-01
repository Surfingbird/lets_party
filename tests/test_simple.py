import asyncio
import pytest
import random
import http

from tests.sub_functions import *
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
    assert respose.status == 200

    data = await respose.json()

    assert type(data) == list
    for item in data:
        product_t.check(item)

    assert respose.status == 200

async def test_get_products_invalid_query1(cli, valid_cookie, new_10_products):
    respose = await cli.get('/products/list', cookies=valid_cookie)
    assert respose.status == 400

async def test_get_products_invalid_query2(cli, valid_cookie, new_10_products):
    params = {
        'start': 1,
        'limit': 'aaasas'
    }
    respose = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert respose.status == 400

async def test_get_products_invalid_query3(cli, valid_cookie, new_10_products):
    params = {
        'start': -1,
        'limit': -1
    }
    respose = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert respose.status == 400

async def test_get_products_with_params(cli, valid_cookie, new_10_products):
    limit = 10
    start = 0

    params = {
        'start': start,
        'limit': limit
    }
    respose = await cli.get('/products/list', cookies=valid_cookie, params=params)
    data = await respose.json()

    assert products_pagination_t.check(data)

    assert len(data['products']) == limit




