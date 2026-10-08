from django.urls import path
from . import views, shop_views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("stages/", views.stages, name="stages"),
    path("stage/<int:number>/", views.start_stage, name="start_stage"),
    path("stage/<int:number>/q/<int:qno>/", views.play_question, name="play_question"),
    path("result/", views.result, name="result"),
    path("book/", views.book, name="book"),
    path("profile/", views.profile, name="profile"),
    path("shop/", shop_views.shop, name="shop"),
    path("shop/buy/", shop_views.buy, name="shop_buy"),
    path("shop/equip/", shop_views.equip, name="shop_equip"),
    path("shop/daily/", shop_views.daily, name="shop_daily"),
    path("shop/unlock/", shop_views.use_unlock, name="shop_unlock"),
    path("use/", shop_views.use_item, name="use_item"),
]
