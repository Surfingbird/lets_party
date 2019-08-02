import asyncio
import pytest
import random
import http

from tests.sub_functions import *
from polls.main_api_app.settings import APP_SECRET, COOKIE_NAME

async def test_get_my_page_success(cli, valid_cookie):
    response = await cli.get('/profile/mypage', cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()
    profile_t.check(data)

async def test_get_my_page_fail(cli):
    response = await cli.get('/profile/mypage')
    assert response.status == 401

async def test_get_my_wishes_simple(cli, valid_cookie):
    response = await cli.get('/profile/mypage/wishes', cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()
    assert len(data) == 0 and type(data) == list

async def test_get_my_wishes_with_wish(cli, valid_cookie, new_product_mongo):
    await cli.post('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : new_product_mongo._id})

    response = await cli.get('/profile/mypage/wishes', cookies=valid_cookie)
    assert response.status == 200

    data = await response.json()
    assert len(data) == 1

    extended_wish_t.check(data[0])


async def test_add_wish_success(cli, valid_cookie, new_product_mongo):
    response = await cli.post('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : new_product_mongo._id})
    assert response.status == 201

async def test_add_wish_bad_request(cli, valid_cookie, new_product_mongo):
    response = await cli.post('/profile/mypage/wishes', cookies=valid_cookie)
    assert response.status == 400

async def test_add_wish_invalid_id(cli, valid_cookie, new_product_mongo):
    response = await cli.post('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : new_product_mongo.product_name})
    assert response.status == 400

async def test_add_wish_not_found(cli, valid_cookie):
    product_id = '5d4293c8de3d25bdbda34c54'

    response = await cli.post('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : product_id})
    assert response.status == 404

async def test_del_wish_success(cli, new_profile_cookie_and_wish_id):
    cookie, product_id = new_profile_cookie_and_wish_id

    response = await cli.delete('/profile/mypage/wishes', cookies=cookie, json={
        'product_id' : product_id})

    assert response.status == 200

    response = await cli.get('/profile/mypage/wishes', cookies=cookie)
    data = await response.json()

    assert len(data) == 0

async def test_del_wish_invalid_product_id(cli, new_profile_cookie_and_wish_id):
    cookie, product_id = new_profile_cookie_and_wish_id

    response = await cli.delete('/profile/mypage/wishes', cookies=cookie, json={
        'product_id' : product_id[::-1]})

    assert response.status == 400

async def test_del_wish_invalid_not_found(cli, valid_cookie, new_product_mongo):
    response = await cli.delete('/profile/mypage/wishes', cookies=valid_cookie, json={
        'product_id' : new_product_mongo._id})

    # TODO maybe change logic
    assert response.status == 200

async def test_del_wish_invalid_no_data(cli, valid_cookie, new_product_mongo):
    response = await cli.delete('/profile/mypage/wishes', cookies=valid_cookie)

    assert response.status == 400

async def test_get_my_intentions_simple(cli, valid_cookie):
    response = await cli.get('/profile/mypage/intentions', cookies=valid_cookie)

    assert response.status == 200
    data = await response.json()

    assert type(data) == list and len(data) == 0

async def test_get_my_intentions_with_intention(cli, cookie_with_intention):
    response = await cli.get('/profile/mypage/intentions', cookies=cookie_with_intention)
    assert response.status == 200
    data = await response.json()

    assert type(data) == list and len(data) == 1
    for intention in data:
        extended_intention_t.check(intention)

async def test_add_intention_success(cli, valid_cookie, profile_vkid_with_wish_and_prod_id):
    dest_id, product_id = profile_vkid_with_wish_and_prod_id

    response = await cli.post('/profile/mypage/intentions', cookies=valid_cookie, json={
        'dest_id' : dest_id,
        'product_id' : product_id
    })

    assert response.status == 201

async def test_add_intention_fail_no_such_wish(cli, valid_cookie, new_product_mongo, new_profile_and_cookie):
    dest_profile, _ = new_profile_and_cookie

    response = await cli.post('/profile/mypage/intentions', cookies=valid_cookie, json={
        'dest_id' : dest_profile['vk_id'],
        'product_id' : new_product_mongo._id
    })

    assert response.status == 404

async def test_add_intention_fail_invalid_data(cli, valid_cookie):
    response = await cli.post('/profile/mypage/intentions', cookies=valid_cookie, json={
        'dest_id' : 'not_vk_id',
        'product_id' : 'not_mongo_id'
    })

    assert response.status == 400








