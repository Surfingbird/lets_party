import asyncio

<<<<<<< HEAD
from polls.models.db import db
=======
from polls.models.db import db, get_mongo_conn
>>>>>>> develop

from bson.objectid import ObjectId
from polls.models.orm_models import Product, Profile

PRODUCTS_ON_PAGE = 10

# TODO реализация транзакций
class ModelManager:
    async def create_product(self, product):
        document = product.to_dict()
        db = get_mongo_conn()

        collection = Product.Meta.collection_name

        res = await db[collection].insert_one(document)

        return str(res.inserted_id)


    # TODO check crunch wish es id 
    async def add_product_in_app(self, product, last_id):
        #TODO append transaction
        pid = await self.create_product(product)
        data = product.to_dict()
        data['p_id'] = pid

        url = db.main_url + str(last_id) + "?pretty"

        async with db.es_session.put(url, json=(data)):
            pass

# TODO FIX BUG
    async def check_wish(self, uid, pid):
        db = get_mongo_conn()

        collection = Profile.Meta.collection_name

        res = await db[collection].find_one({'_id' : ObjectId(uid), 'wishes' : {'p_id' : ObjectId(pid)}})
        if res is None:
            return False
        else:
            return True


    async def check_user(self, uid):
        db = get_mongo_conn()

        collection = Profile.Meta.collection_name

        res = await db[collection].find_one({'_id' : ObjectId(uid)})
        if res is None:
            return False
        else:
            return True


    # TODO написать тест
    async def check_intention(self, uid, pid, dest_id):
        db = get_mongo_conn()

        collection = Profile.Meta.collection_name

        res = await db[collection].find_one({'_id' : ObjectId(uid), 'intentions' : {'product_id' : pid, 'dest_id' : dest_id}})
        if res is None:
            return False
        else:
            return True


    async def check_product(self, pid):
        db = get_mongo_conn()

        collection = Product.Meta.collection_name  

        res = await db[collection].find_one({'_id' : ObjectId(pid)})
        if res is None:
            return False
        else:
            return True


    async def del_profile(self, uid):
        db = get_mongo_conn()

        collection = Profile.Meta.collection_name  

        res = await db[collection].delete_one({'_id' : ObjectId(uid)})
        if res is None:
            return False
        else:
            return True
    

    async def del_product(self, pid):
        db = get_mongo_conn()

        collection = Product.Meta.collection_name  
        
        res = await db[collection].delete_one({'_id' : ObjectId(pid)})
        if res is None:
            return False
        else:
            return True


    # OK
    async def add_users_wish(self, uid, pid):
        product = await Product.objects.get(_id=pid)
        if product is None:
            return False

        profile = await Profile.objects.get(_id=uid)
        if profile is None:
            return False

        collection = Profile.Meta.collection_name

        selector, update = add_users_wish_query(uid, pid)
        db = get_mongo_conn()

        res = await db[collection].update_one(selector, update)
        if res is None:
            return False

        return True

# TODO проверить, корректно и работает
    async def del_users_wish(self, uid, pid):
        product = await Product.objects.get(_id=pid)
        if product is None:
            return False

        profile = await Profile.objects.get(_id=uid)
        if profile is None:
            return False

        # TODO развернуть кластер mongodb
        # async with await db.client.start_session() as s:
        #     async with s.start_transaction():
        s = None
        collection = Profile.Meta.collection_name
        db = get_mongo_conn()

        selector, update = del_users_wish_query(uid, pid)
        res = await db[collection].update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        # TODO FIX
        selector, update = del_users_intention_query_wo_sponsor(uid, pid)
        res = await db[collection].update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        return True

    # OK
    async def get_users_wishes(self, uid):
        res = await Profile.objects.get(_id=uid)
        if res is None:
            return None

        extended_wishes = []

        for wish in res['wishes']:
            product_id = str(wish['product_id'])
            product = await Product.objects.get(_id=product_id)
            if product is not None:
                extended =  {**wish, **product}
                extended_wishes.append(extended)

        return extended_wishes


    # TODO FIX CRUNCH WITH ID
    async def get_users_intentions(self, uid):
        res = await Profile.objects.get(_id=uid)
        if res is None:
            return None

        extended_intentions = []

        for intention in res['intentions']:
            product_id = intention['product_id']
            product = await Product.objects.get(_id=product_id)
            if product is not None:
                extended =  {**intention, **product}
                dest_id = extended['dest_id']
                prof = await Profile.objects.get(_id=dest_id)

                extended['dest_id'] = prof['vk_id']
                
                extended_intentions.append(extended)

        return extended_intentions



    async def intentions_for_user(self, uid, dest_id):
        profile = await Profile.objects.get(_id=uid)
        if profile is None:
            return None

        extended_intentions = []

        for intention in profile['intentions']:
            if dest_id == intention['dest_id']:
                product_id = intention['product_id']
                product = await Product.objects.get(_id=product_id)

                if product is not None:
                    extended =  {**intention, **product}

                    extended_intentions.append(extended)

        return extended_intentions



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

        # TODO развернуть кластер mongodb
        # async with await db.client.start_session() as s:
        #     async with s.start_transaction():
        s = None
        collection = Profile.Meta.collection_name

        selector, update = add_users_intention_query(uid, pid, dest_id)
        db = get_mongo_conn()

        res = await db[collection].update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        selector, update = reserve_users_wish_query(uid, pid, dest_id)
        db = get_mongo_conn()

        res = await db[collection].update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

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

        # TODO развернуть кластер mongodb
        # async with await db.client.start_session() as s:
        #     async with s.start_transaction():
        s = None
        collection = Profile.Meta.collection_name

        condition, update = close_res_users_wish_query(uid, pid, dest_id)
        db = get_mongo_conn()

        res = await db[collection].update_one(condition, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        condition, update = del_users_intention_query(uid, pid, dest_id)
        res = await db[collection].update_one(condition, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        return True
    

# OK
def add_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'wishes' : {'product_id' : pid, 'reserved' : False}}}

def add_users_intention_query(uid, pid, dest_id):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'intentions' : {'product_id' : pid, 'dest_id' : dest_id}}}

def del_users_intention_query(uid, pid, dest_id):
    return {'_id' : ObjectId(uid)}, {'$pull' : {'intentions' : {'product_id' : pid, 'dest_id' : dest_id}}}

def del_users_intention_query_wo_sponsor(uid, pid):
    return {'intentions' : {'$elemMatch' : {'dest_id' : uid, 'product_id' : pid}}}, {'$pull' : {'intentions' : {'product_id' : pid, 'dest_id' : uid}}}

def del_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$pull' : {'wishes' : {'product_id' : pid}}}

def reserve_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.product_id' : pid}, {'$set' : {'wishes.$.reserved' : True, 'wishes.$.sponsor_id' : uid}}

def close_res_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.product_id' : pid}, {'$set' : {'wishes.$.reserved' : False}}
