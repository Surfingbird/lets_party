import trafaret as t
import db

product_t = t.Dict({
    t.Key('_id'): t.Int(),
    t.Key('product_name'): t.String(),
    t.Key('discription'): t.String(),
    t.Key('price'): t.Float(),
    t.Key('img_url'): t.String(),
    t.Key('product_url'): t.String()
})
product_t.make_optional('_id')

def create_product_dict(product_name, discription, price, img_url, product_url):
    document = {
        'product_name': product_name,
        'discription': discription,
        'price': price,
        'img_url': img_url,
        'product_url': product_url
    }
    
    if product_t.check(document):
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