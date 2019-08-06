import asyncio
import pytest
import random
import http

from tests.sub_functions import *
from polls.main_api_app.settings import APP_SECRET, COOKIE_NAME

async def test_get_products(cli, new_product_mongo, valid_cookie):
    response = await cli.get('/products', cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()

    assert type(data) == list
    for item in data:
        product_t.check(item)

    assert response.status == 200

async def test_get_products_invalid_query1(cli, valid_cookie, new_10_products_mongo):
    response = await cli.get('/products/list', cookies=valid_cookie)
    assert response.status == 400

async def test_get_products_invalid_query2(cli, valid_cookie, new_10_products_mongo):
    params = {
        'start': 1,
        'limit': 'aaasas'
    }
    response = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert response.status == 400

async def test_get_products_invalid_query3(cli, valid_cookie, new_10_products_mongo):
    params = {
        'start': -1,
        'limit': -1
    }
    response = await cli.get('/products/list', cookies=valid_cookie, params=params)
    assert response.status == 400

async def test_get_products_with_params(cli, valid_cookie, new_10_products_mongo):
    limit = 10
    start = 0

    params = {
        'start': start,
        'limit': limit
    }
    response = await cli.get('/products/list', cookies=valid_cookie, params=params)
    data = await response.json()

    assert products_pagination_t.check(data)

    assert len(data['products']) == limit


async def test_get_this_product_success(cli, valid_cookie, new_product_mongo):
    response = await cli.get('/products/' + new_product_mongo._id, cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()
    assert product_t.check(data)

async def test_get_this_product_bad_id(cli, valid_cookie):
    response = await cli.get('/products/' + 'there_is_no_this_product', cookies=valid_cookie)
    assert response.status == 400

async def test_get_this_product_not_found(cli, valid_cookie):
    product_id = '5d4293c8de3d25bdbda34c54'

    response = await cli.get('/products/' + product_id, cookies=valid_cookie)
    assert response.status == 404


async def test_get_products_with_pattern_bad_data(cli, valid_cookie):
    response = await cli.get('/products/search', cookies=valid_cookie)
    assert response.status == 400

async def test_get_products_with_pattern_success(cli, valid_cookie, new_product_in_app):
    response = await cli.get('/products/search', cookies=valid_cookie, params={'pattern':new_product_in_app})
    assert response.status == 200

    data = await response.json()
    assert type(data) == list

    for item in data:
        lite_product_t.check(item)

async def test_get_products_with_pattern_fail(cli, valid_cookie, new_product_in_app):
    response = await cli.get('/products/search', cookies=valid_cookie, params={'pattern':new_product_in_app[::-1]})
    assert response.status == 200

    data = await response.json()
    assert type(data) == list
    assert len(data) == 0

async def test_get_products_full_with_pattern_success(cli, valid_cookie, new_product_in_app):
    response = await cli.get('/products/search/result', cookies=valid_cookie, params={'pattern':new_product_in_app})
    assert response.status == 200

    data = await response.json()
    assert type(data) == list

    for item in data:
        product_t.check(item)

async def test_get_products_full_with_pattern_fail(cli, valid_cookie, new_product_in_app):
    response = await cli.get('/products/search/result', cookies=valid_cookie, params={'pattern':new_product_in_app[::-1]})
    assert response.status == 200

    data = await response.json()
    assert type(data) == list
    assert len(data) == 0

async def test_get_my_page_success(cli, valid_cookie):
    response = await cli.get('/profile/mypage', cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()
    profile_t.check(data)

async def test_get_my_page_fail(cli):
    response = await cli.get('/profile/mypage')
    assert response.status == 401




