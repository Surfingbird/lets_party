import asyncio
import pytest
import random
import http

async def test_intention_removed_wish(cli, cookie_with_profile_dict,
    second_cookie_with_profile_dict, new_product_mongo):
        sponsor_cookie, sponsor = cookie_with_profile_dict
        dest_cookie, dest = second_cookie_with_profile_dict

        response = await cli.post('/profile/mypage/wishes', cookies=dest_cookie, json={
            'product_id' : new_product_mongo._id})
        assert response.status == 201

        response = await cli.post('/profile/mypage/intentions', cookies=sponsor_cookie, json={
            'dest_id' : dest['vk_id'],
            'product_id' : new_product_mongo._id
        })
        assert response.status == 201

        response = await cli.delete('/profile/mypage/wishes', cookies=dest_cookie, json={
            'product_id' : new_product_mongo._id})
        assert response.status == 200

        response = await cli.get('/profile/mypage/intentions', cookies=sponsor_cookie)
        assert response.status == 200

        data = await response.json()
        assert len(data) == 0

async def test_wish_removed_intention(cli, cookie_with_profile_dict,
    second_cookie_with_profile_dict, new_product_mongo):
        sponsor_cookie, sponsor = cookie_with_profile_dict
        dest_cookie, dest = second_cookie_with_profile_dict
        
        response = await cli.post('/profile/mypage/wishes', cookies=dest_cookie, json={
            'product_id' : new_product_mongo._id})
        assert response.status == 201

        response = await cli.post('/profile/mypage/intentions', cookies=sponsor_cookie, json={
            'dest_id' : dest['vk_id'],
            'product_id' : new_product_mongo._id
        })
        assert response.status == 201

        response = await cli.get('/profile/mypage/wishes', cookies=dest_cookie)
        assert response.status == 200
        data = await response.json()
        assert data[0]['reserved'] == True

        response = await cli.delete('/profile/mypage/intentions', cookies=sponsor_cookie, json={
            'dest_id' : dest['vk_id'],
            'product_id' : new_product_mongo._id
        })
        assert response.status == 200

        response = await cli.get('/profile/mypage/wishes', cookies=dest_cookie)
        assert response.status == 200
        data = await response.json()
        assert data[0]['reserved'] == False










