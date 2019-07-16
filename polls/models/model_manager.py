from polls.models import db
from bson.objectid import ObjectId
import asyncio

def add_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'wishes' : {'p_id' : ObjectId(pid), 'reserved' : False}}}

def add_users_intention_query(uid, pid, dest_id):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'intentions' : {'p_id' :  ObjectId(pid), 'dest_id' : ObjectId(dest_id)}}}

def del_users_intention_query(uid, pid, dest_id)
    return {'_id' : ObjectId(uid)}, {'$pull' : {'wishes' : {'p_id' : ObjectId(pid), 'dest_id' : ObjectId(dest_id)}}}

def reserve_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.p_id' : ObjectId(pid)}, {'$set' : {'wishes.$.reserved' : True, 'wishes.$.sponsor_id' : ObjectId(uid)}}

# TODO описать логику проверки поля reserved, чтобы не перезаписывать спонсора
def close_res_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.p_id' : ObjectId(pid)}, {'$set' : {'wishes.$.reserved' : False}


# TODO реализация транзакций
class ProfileManager:
    async def check_wish(self, uid, pid):
        res = await db.profiles_collection.find_one({'_id' : ObjectId(uid)})

    async def check_user(self, uid):
        res = await db.profiles_collection.find_one({'_id' : ObjectId(uid)})
        if res is None:
            return False
        else:
            return True

    async def check_intention(self, uid, pid, dest_id):
        res = await db.profiles_collection.find_one({'_id' : ObjectId(uid), 'intentions' : {'p_id' : ObjectId(pid), 'dest_id' : ObjectId(dest_id)}})
        if res is None:
            return False
        else:
            return True

    async def check_product(self, pid):
        res = await db.product_collection.find_one({'_id' : ObjectId(pid)})
        if res is None:
            return False

        return True

    async def add_users_wish(self, uid, pid):
        res = await self.check_product(pid)
        if res is None:
            return False

        res = await self.check_user(uid)
        if res is None:
            return False

        query = add_users_wish_query(uid, pid)
        res = await db.profiles_collection.update_one(query)
        if res is None:
            return False

        return True

    async def del_users_wish(self, uid, pid):
        res = await self.check_user(uid)
        if res is None:
            return False

        pass

    async def add_users_intention(self, uid, pid, dest_id):
        res = await self.check_user(uid)
        if res is None:
            return False

        res = await self.check_user(dest_id)
        if res is None:
            return False

        res = await self.check_wish(dest_id, pid)
        if res is None:
            return False

        query = add_users_intention_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(query)
        if res is None:
            return False

        condition, update = reserve_users_wish_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(condition, update)
        if res is None:
            return False

        return True

    async def del_users_intention(self, uid, pid, dest_id):
        res = await self.check_user(uid)
        if res is None:
            return False

        res = await self.check_user(dest_id)
        if res is None:
            return False

        res = await self.check_intention(uid, pid, dest_id)
        if res is None:
            return False

        # TODO еще нужно убрать пронирование подарка
        res = await self.check_intention(uid, pid, dest_id)
        if res is None:
            return False

        condition, update = close_res_users_wish_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(condition, update)
        if res is None:
            return False

        condition, update = del_users_intention_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(condition, update)
        if res is None:
            return False

        return True
    
# db.getCollection('profiles').update( {_id : ObjectId("5d2cca26e6f19f24a6a9fd2a")}, {$push : {wishes : ObjectId("5d2c7cf436e8a861bb87a942")}} )
# db.getCollection('profiles').update( {_id : ObjectId("5d2cca26e6f19f24a6a9fd2a")}, {$pull : {wishes : ObjectId("5d2c7cf436e8a861bb87a942")}} )

# loop = asyncio.get_event_loop()
# loop.run_until_complete(add_users_wish_queery("5d2cca26e6f19f24a6a9fd2a", "5d2c7cf436e8a861bb87a941"))

# res = reserve_users_wish_query("5d2cca26e6f19f24a6a9fd2a", "5d2c7cf436e8a861bb87a941", "5d2c7cf436e8a861bb87a941")
# print(type(res), res)
# condition, update = reserve_users_wish_query("5d2cca26e6f19f24a6a9fd2a", "5d2c7cf436e8a861bb87a941", "5d2c7cf436e8a861bb87a941")
# print(type(condition), condition)
    