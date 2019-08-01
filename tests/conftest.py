import pytest
import asyncio
from aiohttp.test_utils import loop_context
import motor.motor_asyncio

from polls.main_api_app.main import create_app
from polls.models.orm_models import Profile
from polls.models.fake_model_manager import FakeModelManager
from polls.models.db import client

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
    yield create_app(loop=event_loop, dbname=TESTDATABASE)

@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client

# @pytest.fixture(scope='function')
# async def new_profile(event_loop, app):
#     profile = await fm._create_fake_profile()
#     yield profile
#     await profile.delete()
