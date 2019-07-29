import views

from aiohttp import web

def setup_routes(app):
    app.router.add_post('/auth', views.login)
    app.router.add_delete('/auth', views.logout)

    app.router.add_get('/products', views.new_products)
    app.router.add_get('/products/list', views.products_list)
    app.router.add_get('/products/search', views.search_products)
    app.router.add_get('/products/{id}', views.product)

    app.router.add_get('/profile/mypage', views.mypage)

    app.router.add_get('/profile/mypage/wishes', views.my_wishes)
    app.router.add_post('/profile/mypage/wishes', views.add_my_wishe)
    app.router.add_delete('/profile/mypage/wishes', views.del_my_wishe)

    app.router.add_get('/profile/mypage/intentions', views.my_intentions)
    app.router.add_post('/profile/mypage/intentions', views.add_my_intentions)
    app.router.add_delete('/profile/mypage/intentions', views.del_my_intentions)

    app.router.add_get('/profile/{dest_id}/wishes', views.users_wishes)
    app.router.add_get('/profile/{dest_id}/intentions', views.intentions_for_user)


