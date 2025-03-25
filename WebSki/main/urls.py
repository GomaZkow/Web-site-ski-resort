from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ski-trail/', views.ski_trail, name='ski-trail'),
    path('ski-pass/', views.ski_pass, name='ski-pass'),
    path('events/', views.events, name='events'),
    path('photos/', views.photos, name='photos'),
    path('reviews/', views.reviews, name='reviews'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
