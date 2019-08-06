import asyncio
import pytest
import random
import http

from tests.sub_functions import *
from polls.main_api_app.settings import APP_SECRET, COOKIE_NAME

async def test_auth_success(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    response = await cli.post('/auth', json = {'url':url})
    assert response.status == 200

async def test_auth_fail(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    response = await cli.post('/auth', json = {'url':url})
    assert response.status == 401

async def test_auth_invali_request_another_data(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    response = await cli.post('/auth', data='test_auth_invali_request_another_data')
    assert response.status == 400

async def test_auth_invali_request_empty_data(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, secret=APP_SECRET + 'smth_more')

    response = await cli.post('/auth')
    assert response.status == 400

async def test_unauth_success(cli):
    vk_id = random.randint(1, 1000000000)
    url = gen_vk_url(vk_id, APP_SECRET)

    response = await cli.post('/auth', json = {'url':url})
    cookie = response.cookies[COOKIE_NAME]
    cookie_data = {'value' : cookie.value}

    response = await cli.delete('/auth', cookies={'value' : cookie.value})
    assert response.status == 200
