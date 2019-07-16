# import pytest
import asyncio

from polls.models import fake_model_manager as fmm

fm = fmm.FakeModelManager()

# @pytest.mark.asyncio
async def test_check_profile():
    res = await fm._create_fake_profile()
    print(type(res.inserted_id), res.inserted_id)

async def run_all_tests():
    await test_check_profile()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_all_tests())

