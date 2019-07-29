import asyncio

from polls.orm.db import db
from polls.models import api

from bson.objectid import ObjectId
from polls.models.orm_models import Product, Profile


def create_product_dict(product_name, discription, price, img_url, product_url):
    document = {}

    if discription: 
        document = {
            'product_name': product_name,
            'discription': discription,
            'price': price,
            'img_url': img_url,
            'product_url': product_url
        }
    else :
        document = {
            'product_name': product_name,
            'price': price,
            'img_url': img_url,
            'product_url': product_url
        }
    
    if api.product_t.check(document):
        return document


PRODUCTS_ON_PAGE = 10

# TODO реализация транзакций
class ModelManager:
    async def create_product(self, product):
        document = product.to_dict()
        res = await db.product_collection.insert_one(document)

        return str(res.inserted_id)


    # TODO check crunch wish es id 
    async def add_product_in_app(self, product, last_id):
        #TODO append transaction
        pid = await self.create_product(product)
        data = product.to_dict()
        data['p_id'] = pid

        url = db.main_url + str(last_id) + "?pretty"

        async with db.es_session.put(url, json=(data)) as resp:
            #  print(await resp.text())
            pass


    async def get_products(self):
        return await db.product_collection.find().limit(PRODUCTS_ON_PAGE).to_list(length=PRODUCTS_ON_PAGE)


    # TODO написать тест
    async def check_wish(self, uid, pid):
        res = await db.profiles_collection.find_one({'_id' : ObjectId(uid), 'wishes' : {'p_id' : ObjectId(pid)}})
        if res is None:
            return False
        else:
            return True

    
    async def get_profile(self, uid):
        return await db.profiles_collection.find_one({'_id' : ObjectId(uid)})


    async def get_product(self, pid):
        return await db.product_collection.find_one({'_id' : ObjectId(pid)})


    async def check_user(self, uid):
        res = await db.profiles_collection.find_one({'_id' : ObjectId(uid)})
        if res is None:
            return False
        else:
            return True


    # TODO написать тест
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
        else:
            return True


    async def del_profile(self, uid):
        res = await db.profiles_collection.delete_one({'_id' : ObjectId(uid)})
        if res is None:
            return False
        else:
            return True
    

    async def del_product(self, pid):
        res = await db.product_collection.delete_one({'_id' : ObjectId(pid)})
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
        res = await db[collection].update_one(selector, update)
        if res is None:
            return False

        return True

# TODO проверить, корректно и работает
    async def del_users_wish(self, uid, pid):
        res = await self.check_user(uid)
        if res is None:
            return False

        res = await self.check_wish(uid, pid)
        if res is None:
            return False

        # TODO развернуть кластер mongodb
        # async with await db.client.start_session() as s:
        #     async with s.start_transaction():
        s = None

        selector, update = del_users_wish_query(uid, pid)
        res = await db.profiles_collection.update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        selector, update = del_users_intention_query_wo_sponsor(uid, pid)
        res = await db.profiles_collection.update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        return True

    async def get_users_wishes(self, uid):
        res = await self.get_profile(uid)
        if res is None:
            return None

        extended_wishes = []

        for wish in res['wishes']:
            str_id = str(wish['p_id'])
            product = await self.get_product(str_id)
            if product is not None:
                extended =  {**wish, **product}
                extended['p_id'] = str_id
                extended['_id'] = str_id
                extended['sponsor_id'] = uid

                extended_wishes.append(extended)

        return extended_wishes

    async def get_users_intentions(self, uid):
        res = await self.get_profile(uid)
        if res is None:
            return None

        extended_intentions = []

        for intention in res['intentions']:
            str_id = str(intention['p_id'])
            product = await self.get_product(str_id)
            if product is not None:
                extended =  {**intention, **product}
                extended['p_id'] = str_id
                extended['_id'] = str_id

                extended_intentions.append(extended)

        return extended_intentions

    async def intentions_for_user(self, uid, dest_id):
        res = await self.get_profile(uid)
        if res is None:
            return None

        extended_intentions = []

        for intention in res['intentions']:
            str_dest_id = str(intention['dest_id'])
            if str_dest_id == dest_id:
                str_p_id = str(intention['p_id'])

                product = await self.get_product(str_p_id)
                if product is not None:
                    extended =  {**intention, **product}
                    extended['p_id'] = str_p_id
                    extended['_id'] = str_p_id
                    extended['dest_id'] = str_dest_id

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

        selector, update = add_users_intention_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(selector, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        selector, update = reserve_users_wish_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(selector, update, session=s)
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

        res = await self.check_intention(uid, pid, dest_id)
        if res is None:
            return False

        # TODO развернуть кластер mongodb
        # async with await db.client.start_session() as s:
        #     async with s.start_transaction():
        s = None

        condition, update = close_res_users_wish_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(condition, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        condition, update = del_users_intention_query(uid, pid, dest_id)
        res = await db.profiles_collection.update_one(condition, update, session=s)
        if res is None:
            # await s.abort_transaction()

            return False

        return True
    

# OK
def add_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'wishes' : {'product_id' : pid, 'reserved' : False}}}

def add_users_intention_query(uid, pid, dest_id):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'intentions' : {'p_id' :  ObjectId(pid), 'dest_id' : ObjectId(dest_id)}}}

def del_users_intention_query(uid, pid, dest_id):
    return {'_id' : ObjectId(uid)}, {'$pull' : {'intentions' : {'p_id' : ObjectId(pid), 'dest_id' : ObjectId(dest_id)}}}

def del_users_intention_query_wo_sponsor(uid, pid):
    return {}, {'$pull' : {'wishes' : {'p_id' : ObjectId(pid), 'dest_id' : ObjectId(uid)}}}

def del_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$pull' : {'wishes' : {'p_id' : ObjectId(pid)}}}


def reserve_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.p_id' : ObjectId(pid)}, {'$set' : {'wishes.$.reserved' : True, 'wishes.$.sponsor_id' : ObjectId(uid)}}

# TODO описать логику проверки поля reserved, чтобы не перезаписывать спонсора
def close_res_users_wish_query(uid, pid, dest_id):
    return {'_id': ObjectId(dest_id), 'wishes.p_id' : ObjectId(pid)}, {'$set' : {'wishes.$.reserved' : False}}
