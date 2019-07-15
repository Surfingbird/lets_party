import trafaret as t

product_t = t.Dict({
    t.Key('_id'): t.Int(),
    t.Key('product_name'): t.String(),
    t.Key('discription'): t.String(),
    t.Key('price'): t.Float(),
    t.Key('img_url'): t.String(),
    t.Key('product_url'): t.String()
})
product_t.make_optional('_id')
product_t.make_optional('discription')

wish_t = t.Dict({
    t.Key('product_id'): t.String(),
    t.Key('sponsor_id'): t.Int(),
    t.Key('reserved'): t.Bool()
})
wish_t.make_optional('sponsor_id')

intention_t = t.Dict({
    t.Key('product_id'): t.String(),
    t.Key('inst_id'): t.Int(),
    t.Key('recipient_id'): t.Int(),
})

profile_t = t.Dict({
    t.Key('uid'): t.Int(),
    t.Key('first_name'): t.String(),
    t.Key('last_name'): t.String(),
    t.Key('photo_url'): t.String(),
    t.Key('wishes'): t.List(wish_t),
    t.Key('intentions'): t.List(intention_t)
})