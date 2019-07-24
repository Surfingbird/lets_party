import asyncio
import inspect 
import motor.motor_asyncio

from bson.objectid import ObjectId
from fields import Field, StringField, IntField
from query_set import QuerySet
from manager import Manage

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client['kts_orm']

class Model:
    objects = Manage()
    _id = StringField(required=False, default='')

    def __init__(self):
        self.obj_schema = dict()

        for key, value in inspect.getmembers(self):
            if issubclass(type(value), Field):
                self.obj_schema[key] = value


    def __str__(self):
        return str(self._get_dicts_schema())


    def _check(self):
        for key in self.obj_schema:
            self.obj_schema[key].validate()


    def _get_dicts_schema(self):
        res = dict()

        for key in self.obj_schema:
            res[key] = self.obj_schema[key].get()

        return res
        

    async def save(self):
        collection = self.Meta.collection_name
        data = self._get_dicts_schema()
        data.pop('_id', data)

        res = await db[collection].insert_one(data)
        self._id.required = True
        self._id.set_val(str(res.inserted_id))


    async def update(self, **kwargs):
        collection = self.Meta.collection_name

        updated_doc = dict()

        for key in kwargs:
            self.obj_schema[key].set_val(kwargs[key])
            self.obj_schema[key].validate()

            updated_doc[key] = kwargs[key]

        _id = self.obj_schema['_id'].get()

        await db[collection].update_one({'_id' : ObjectId(_id)}, {'$set' : updated_doc})


    async def delete(self):
        collection = self.Meta.collection_name
        _id = self.obj_schema['_id'].get()

        await db[collection].delete_one({'_id' : ObjectId(_id)})



class Profile(Model):
    _id = StringField(required=False, default='')
    first_name = StringField()
    last_name = StringField()

    def __init__(self, *args, **kwargs):
        super().__init__()

        for key in kwargs:
            self.obj_schema[key].set_val(kwargs[key])

        super()._check()

    class Meta:
        collection_name = 'orm_profiles'

async def main():
    m = Profile(first_name='121', last_name='1er1')
    await m.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())




