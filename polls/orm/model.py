import asyncio
import inspect 

from bson.objectid import ObjectId
from fields import Field, StringField, IntField
from query_set import QuerySet
from manager import Manage

from db import db

class Model:
    objects = Manage()

    _id = StringField(required=False, default='')


    def __init__(self, **kwargs):
        self.changed = None

        for key, value in inspect.getmembers(self):
            if issubclass(type(value), Field):
                self.__dict__[key] = value.default


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

            res = await db[collection].insert_one(document)
            self._id = (str(res.inserted_id))

        elif self.changed == True:
            document = self.__dict__.copy()

            _id = document.pop('_id', document)
            document.pop('changed', document)

            await db[collection].update_one({'_id' : ObjectId(_id)}, {'$set' : document})
            self.changed = False


    async def delete(self):
        collection = self.Meta.collection_name
        _id = self.__dict__['_id']

        await db[collection].delete_one({'_id' : ObjectId(_id)})


class Profile(Model):
    _id = StringField(required=False, default='')
    first_name = StringField()
    last_name = StringField()

    class Meta:
        collection_name = 'orm_profiles'