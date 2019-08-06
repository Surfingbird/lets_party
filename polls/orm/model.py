import asyncio
import inspect 

from bson.objectid import ObjectId
from polls.orm.fields import Field, StringField, IntField, ListField
from polls.orm.query_set import QuerySet
from polls.orm.manager import Manage

<<<<<<< HEAD
from polls.models.db import db
=======
from polls.models.db import db, get_mongo_conn
>>>>>>> develop

class Model:
    objects = Manage()


    def __init__(self, **kwargs):
        self.changed = None

        for key, value in inspect.getmembers(self):
            if issubclass(type(value), Field) or issubclass(type(value), ListField):
                self.__dict__[key] = value.default

        for key, value in kwargs.items():
            self.__class__.__dict__[key].validate(value)
            self.__dict__[key] = value


    def __str__(self):
        return str(self.__dict__)


    def __setattr__(self, name, value):
        if name == 'changed':
            self.__dict__[name] = value

            return

        self.__class__.__dict__[name].validate(value)
        if not value == self.__dict__[name]:
            self.__dict__[name] = value
            self.__dict__['changed'] = True


    async def save(self):
        collection = self.Meta.collection_name

        if self.changed is None:
            document = self.__dict__.copy()
            
            document.pop('_id', document)
            document.pop('changed', document)
            
            db = get_mongo_conn()
            res = await db[collection].insert_one(document)
            self._id = (str(res.inserted_id))

        elif self.changed == True:
            document = self.__dict__.copy()

            _id = document.pop('_id', document)
            document.pop('changed', document)

            db = get_mongo_conn()

            await db[collection].update_one({'_id' : ObjectId(_id)}, {'$set' : document})
            self.changed = False


    async def delete(self):
        collection = self.Meta.collection_name
        _id = self.__dict__['_id']

<<<<<<< HEAD
        await db[collection].delete_one({'_id' : ObjectId(_id)})
=======
        db = get_mongo_conn()

        await db[collection].delete_one({'_id' : ObjectId(_id)})
>>>>>>> develop
