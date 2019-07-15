import datetime
import trafaret as t

product = t.Dict({
    t.Key('_id'): t.Int(),
    t.Key('product_name'): t.String(),
    t.Key('discription'): t.String(),
    t.Key('price'): t.Float(),
    t.Key('img_url'): t.String()
})
product.make_optional('_id')

wish = t.Dict({
    t.Key('product_id'): t.String(),
    t.Key('sponsor_id'): t.Int(),
    t.Key('reserved'): t.Bool()
})
wish.make_optional('sponsor_id')

intention = t.Dict({
    t.Key('product_id'): t.String(),
    t.Key('inst_id'): t.Int(),
    t.Key('recipient_id'): t.Int(),
})

profile = t.Dict({
    t.Key('uid'): t.Int(),
    t.Key('first_name'): t.String(),
    t.Key('last_name'): t.String(),
    t.Key('photo_url'): t.String(),
    t.Key('wishes'): t.List(wish),
    t.Key('intentions'): t.List(intention)
})

def create_product(product_name, discription, price, img_url):
    document = {
        'product_name': product_name,
        'discription': discription,
        'price': price,
        'img_url': img_url
    }
    
    if product.check(document):
        return document