from polls.models import db
from polls.models import api
from bson.objectid import ObjectId

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

class ProductManager:
    async def create_product(self, product):
        document = product.to_dict()
        await db.product_collection.insert_one(document)

    async def del_product(self, _id):
        pass

    async def get_product(self, _id):
        return await db.product_collection.find_one({'_id' : ObjectId(_id)})