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


async def test_get_products(cli, new_product_mongo, valid_cookie):
    respose = await cli.get('/products', cookies=valid_cookie)
    assert respose.status == 200

    data = await respose.json()

    assert type(data) == list
    for item in data:
        product_t.check(item)

    assert respose.status == 200

async def test_get_products_invalid_query1(cli, valid_cookie, new_10_products_mongo):
    respose = await cli.get('/products/list', cookies=valid_cookie)
    assert respose.status == 400

async def test_get_products_invalid_query2(cli, valid_cookie, new_10_products_mongo):
    params = {
        'start': 1,
        'limit': 'aaasas'
    }
    respose = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert respose.status == 400

async def test_get_products_invalid_query3(cli, valid_cookie, new_10_products_mongo):
    params = {
        'start': -1,
        'limit': -1
    }
    respose = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert respose.status == 400

async def test_get_products_with_params(cli, valid_cookie, new_10_products_mongo):
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


async def test_get_this_product_success(cli, valid_cookie, new_product_mongo):
    respose = await cli.get('/products/' + new_product_mongo._id, cookies=valid_cookie)
    assert respose.status == 200

    data = await respose.json()
    assert product_t.check(data)

async def test_get_this_product_bad_id(cli, valid_cookie):
    respose = await cli.get('/products/' + 'there_is_no_this_product', cookies=valid_cookie)
    assert respose.status == 400

async def test_get_this_product_not_found(cli, valid_cookie):
    product_id = '5d4293c8de3d25bdbda34c54'

    respose = await cli.get('/products/' + product_id, cookies=valid_cookie)
    assert respose.status == 404


async def test_get_products_with_pattern_bad_data(cli, valid_cookie):
    respose = await cli.get('/products/search', cookies=valid_cookie)
    assert respose.status == 400

async def test_get_products_with_pattern_success(cli, valid_cookie, new_product_in_app):
    respose = await cli.get('/products/search', cookies=valid_cookie, params={'pattern':new_product_in_app})
    assert respose.status == 200

    data = await respose.json()
    assert type(data) == list

    for item in data:
        lite_product_t.check(item)

async def test_get_products_with_pattern_fail(cli, valid_cookie, new_product_in_app):
    respose = await cli.get('/products/search', cookies=valid_cookie, params={'pattern':new_product_in_app[::-1]})
    assert respose.status == 200

    data = await respose.json()
    assert type(data) == list
    assert len(data) == 0

async def test_get_products_full_with_pattern_success(cli, valid_cookie, new_product_in_app):
    respose = await cli.get('/products/search/result', cookies=valid_cookie, params={'pattern':new_product_in_app})
    assert respose.status == 200

    data = await respose.json()
    assert type(data) == list

    for item in data:
        product_t.check(item)

async def test_get_products_full_with_pattern_fail(cli, valid_cookie, new_product_in_app):
    respose = await cli.get('/products/search/result', cookies=valid_cookie, params={'pattern':new_product_in_app[::-1]})
    assert respose.status == 200

    data = await respose.json()
    assert type(data) == list
    assert len(data) == 0


