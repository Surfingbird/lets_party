import views

from aiohttp import web

def setup_routes(app):
    app.router.add_get('/events', views.near_events)
    app.router.add_get('/events/popular', views.popular_events)
    app.router.add_get('/events/search', views.search_events)
    app.router.add_get('/events/{slug}', views.event)
    app.router.add_get('/events/search/{pattern}', views.get_events)

    app.router.add_get('/profile/mypage', views.mypage)

    app.router.add_get('/profile/mypage/wishes', views.my_wishes)
    app.router.add_post('/profile/mypage/wishes', views.add_my_wishe)
    app.router.add_delete('/profile/mypage/wishes', views.del_my_wishe)

    app.router.add_get('/profile/mypage/intentions', views.my_intentions)
    app.router.add_post('/profile/mypage/intentions', views.add_my_intentions)
    app.router.add_delete('/profile/mypage/intentions', views.del_my_intentions)

    app.router.add_get('/profile/{nick_or_id}/wishes', views.users_wishes)
    app.router.add_get('/profile/{nick_or_id}/intentions', views.intentions_for_user)


