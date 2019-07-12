import datetime
import trafaret as t

instance = t.Dict({
    t.Key('id'): t.Int(),
    t.Key('date'): t.String(),
    t.Key('time'): t.String(),
    t.Key('min_price'): t.Float(),
    t.Key('img_url'): t.String()
})
instance.make_optional('min_price')

event = t.Dict({
    # ToDo нужна генерация slug
    # t.Key('slug'): t.String(),
    t.Key('name'): t.String(),
    t.Key('discription'): t.String(),
    t.Key('instances'): t.List(instance)
})
event.make_optional('_id')

def create_instance(_id, date, time, min_price, img_url):
    document = {
        'id': _id,
        'date': date,
        'time': time,
        'min_price': min_price,
        'img_url': img_url
    }
    
    if instance.check(document):
        return document

def create_event(name, discription, insts):    
    document = {
        'name': name,
        'discription': discription,
        'instances': insts
    }
    
    if event.check(document):
        return document