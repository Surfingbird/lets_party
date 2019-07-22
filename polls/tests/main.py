import asyncio
import pytest

from bson.objectid import ObjectId

from polls.models import fake_model_manager as fmm
from polls.models import model_manager

fm = fmm.FakeModelManager()
mm = model_manager.ModelManager()

def test_check_profile_simple():
    loop = asyncio.get_event_loop()

    async def inner_check_profile_simple():
        res = await fm._create_fake_profile()
        assert res is not  None

        ok = await mm.check_user(res.inserted_id)
        assert ok == True

        ok = await mm.del_profile(res.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_check_profile_simple())


def test_check_product_simple():
    loop = asyncio.get_event_loop()

    async def inner_check_product_simple():
        res = await fm._create_fake_product()
        assert res is not  None

        ok = await mm.check_product(res.inserted_id)
        assert ok == True

        ok = await mm.del_product(res.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_check_product_simple())


def test_add_users_wish_simple():
    loop = asyncio.get_event_loop()

    async def inner_add_users_wish_simple():
        product = await fm._create_fake_product()
        assert product is not  None
        profile = await fm._create_fake_profile()
        assert profile is not  None

        await mm.add_users_wish(profile.inserted_id, product.inserted_id)
        updated_profile = await mm.get_profile(profile.inserted_id)
        assert updated_profile is not None
        assert len(updated_profile['wishes']) == 1

        ok = await mm.del_product(product.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_add_users_wish_simple())


def test_del_users_wish_simple():
    loop = asyncio.get_event_loop()

    async def inner_del_users_wish_simple():
        product = await fm._create_fake_product()
        assert product is not  None
        profile = await fm._create_fake_profile()
        assert profile is not  None

        await mm.add_users_wish(profile.inserted_id, product.inserted_id)
        ok = await mm.del_users_wish(profile.inserted_id, product.inserted_id)
        assert ok == True

        updated_profile = await mm.get_profile(profile.inserted_id)
        assert len(updated_profile['wishes']) == 0

        ok = await mm.del_product(product.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_del_users_wish_simple())


def test_add_users_intention_full():
    loop = asyncio.get_event_loop()

    async def inner_add_users_intention_full():
        product = await fm._create_fake_product()
        assert product is not  None
        profile_from = await fm._create_fake_profile()
        assert profile_from is not  None
        profile_to = await fm._create_fake_profile()
        assert profile_to is not  None

        ok = await mm.add_users_wish(profile_to.inserted_id, product.inserted_id)
        assert ok == True

        ok = await mm.add_users_intention(profile_from.inserted_id, product.inserted_id, profile_to.inserted_id)
        assert ok == True

        updated_from_prof = await mm.get_profile(profile_from.inserted_id)
        updated_to_prof = await mm.get_profile(profile_to.inserted_id)

        assert len(updated_from_prof['intentions']) == 1
        assert updated_to_prof['wishes'][0]['reserved'] == True
        assert updated_to_prof['wishes'][0]['sponsor_id'] == ObjectId(profile_from.inserted_id)

        ok = await mm.del_product(product.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile_from.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile_to.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_add_users_intention_full())


def test_del_users_intention_full():
    loop = asyncio.get_event_loop()

    async def inner_del_users_intention_full():
        product = await fm._create_fake_product()
        assert product is not  None
        profile_from = await fm._create_fake_profile()
        assert profile_from is not  None
        profile_to = await fm._create_fake_profile()
        assert profile_to is not  None

        ok = await mm.add_users_wish(profile_to.inserted_id, product.inserted_id)
        assert ok == True

        ok = await mm.add_users_intention(profile_from.inserted_id, product.inserted_id, profile_to.inserted_id)
        assert ok == True

        ok = await mm.del_users_intention(profile_from.inserted_id, product.inserted_id, profile_to.inserted_id)
        assert ok == True

        updated_from_prof = await mm.get_profile(profile_from.inserted_id)
        updated_to_prof = await mm.get_profile(profile_to.inserted_id)

        assert len(updated_from_prof['intentions']) == 0
        assert updated_to_prof['wishes'][0]['reserved'] == False

        ok = await mm.del_product(product.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile_from.inserted_id)
        assert ok == True
        ok = await mm.del_profile(profile_to.inserted_id)
        assert ok == True

    loop.run_until_complete(inner_del_users_intention_full())


# TODO тут баг
# def test_del_users_wish_full():
#     loop = asyncio.get_event_loop()

#     async def inner_del_users_wish_full():
#         product = await fm._create_fake_product()
#         assert product is not  None
#         profile_from = await fm._create_fake_profile()
#         assert profile_from is not  None
#         profile_to = await fm._create_fake_profile()
#         assert profile_to is not  None

#         ok = await mm.add_users_wish(profile_to.inserted_id, product.inserted_id)
#         assert ok == True

#         ok = await mm.add_users_intention(profile_from.inserted_id, product.inserted_id, profile_to.inserted_id)
#         assert ok == True

#         ok = await mm.del_users_wish(profile_to.inserted_id, product.inserted_id)
#         assert ok == True

#         updated_from_prof = await mm.get_profile(profile_from.inserted_id)
#         updated_to_prof = await mm.get_profile(profile_to.inserted_id)

#         assert len(updated_to_prof['wishes']) == 0
#         assert len(updated_from_prof['intentions']) == 0

#         ok = await mm.del_product(product.inserted_id)
#         assert ok == True
#         ok = await mm.del_profile(profile_from.inserted_id)
#         assert ok == True
#         ok = await mm.del_profile(profile_to.inserted_id)
#         assert ok == True

#     loop.run_until_complete(inner_del_users_wish_full())