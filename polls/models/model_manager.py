from polls.models import db
from polls.models import api

from bson.objectid import ObjectId
import asyncio


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


class Product:
    def __init__(self, product_name, discription, price, img_url, product_url):
        self.product_name = product_name
        self.discription = discription
        self.price = price
        self.img_url = img_url
        self.product_url = product_url
        
    def to_dict(self):
        document = create_product_dict(self.product_name, self.discription, self.price, self.img_url, self.product_url)
        return document

    def __str__(self):
        res = f"name = {self.product_name}, discription = {self.discription}, price = {self.price}, img_url = {self.img_url}, product_url = {self.product_url}"
        
        return res


PRODUCTS_ON_PAGE = 10

# TODO реализация транзакций
class ModelManager:
    async def create_product(self, product):
        document = product.to_dict()
        await db.product_collection.insert_one(document)


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


    async def add_users_wish(self, uid, pid):
        res = await self.check_product(pid)
        if res is None:
            return False

        res = await self.check_user(uid)
        if res is None:
            return False

        selector, update = add_users_wish_query(uid, pid)
        res = await db.profiles_collection.update_one(selector, update)
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

                extended_wishes.append(extended)

        return extended_wishes


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
    

def add_users_wish_query(uid, pid):
    return {'_id' : ObjectId(uid)}, {'$addToSet' : {'wishes' : {'p_id' : ObjectId(pid), 'reserved' : False}}}

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
