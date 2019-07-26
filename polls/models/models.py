from polls.orm.fields import StringField, ListField, BoolField, InnerObject, IntField
from polls.orm.model import Model

class Wish(InnerObject):
    reserved = BoolField(required=True, default=False)
    sponsor_id = StringField(required=False, default='')
    product_id = StringField(required=True, default='')

    def __init__(self):
        super().__init__(self.__class__)

class WishListField(ListField):
    item_type = Wish()


class Intention(InnerObject):
    product_id = StringField(required=True, default='')
    dest_id = StringField(required=False, default='')

    def __init__(self):
        super().__init__(self.__class__)

class IntentionListField(ListField):
    item_type = Intention()


class Profile(Model):
    vk_id = IntField(required=True, default=None)
    first_name = StringField(required=True, default=None)
    last_name = StringField(required=True, default=None)
    photo_url = StringField(required=False, default='')
    wishes = WishListField()
    intentions = IntentionListField()

    class Meta:
        collection_name = 'profiles'

    
class Product(Model):
    product_name = StringField(required=True, default=None)
    discription = StringField(required=False, default='')
    price = IntField(required=True, default=None)
    img_url = StringField(required=False, default='')
    product_url = StringField(required=True, default=None)

    class Meta:
        collection_name = 'products'