from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("shop/<str:gender>/", views.shop_gender, name="shop_gender"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.wishlist_toggle, name="wishlist_toggle"),
    path("orders/", views.order_history, name="order_history"),
    path("collections/", views.collections, name="collections"),
    path("basics/", views.basics, name="basics"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/<str:action>/", views.cart_update, name="cart_update"),
    path("sale/", views.sale, name="sale"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("", include("django.contrib.auth.urls")),
    path("checkout/", views.checkout, name="checkout"), 

    # auth personalizados
    path("signup/", views.signup, name="signup"),
    path("account/", views.account, name="account"),
]
