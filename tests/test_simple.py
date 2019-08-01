import asyncio
import pytest
import random

from tests.sub_functions import gen_vk_url
from polls.main_api_app.settings import APP_SECRET

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