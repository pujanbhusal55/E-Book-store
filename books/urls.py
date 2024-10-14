from numpy import delete
from books import views



from. import views
from django.contrib.auth import views as auth_views
from django.conf import settings

from numpy import delete
from books import views
from django.urls import path


from django.contrib.auth import views as auth_views
from users.views import home
from numpy import delete
from books import views
from django.urls import path
from . import views
from django.urls import path, include
from .views import (
  
    addwishlist,
    removewishlist,
    wishdetails,
    my_books,
    
    
)

urlpatterns = [
    path('', home, name='users-home'),
    path('store/', views.store, name='store'),
    path('search/', views.search, name='search'), 
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
      
    path('delete-account/', views.delete_account, name='delete_account'),

    #path('addcart/<int:book_id>/', addcart, name='addcart'),
    #path('removecart/<int:id>/', removecart, name='removecart'),
    #path('cart/', cartdetails, name='cartdetails'),
    path('addwishlist/<int:book_id>/', addwishlist, name='addwishlist'),
    path('removewishlist/<int:id>/', removewishlist, name='removewishlist'),
    path('wishdetails/', wishdetails, name='wishdetails'),
    #path('checkout/', views.checkout, name='checkout'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('mybook/', views.my_books, name = 'my_books'),
    #path('removepurchasedbook/<int:id>/', removepurchasedbook, name='removepurchasedbook'),
    path('buybook/<int:id>/', views.buybook, name='buybook'),
    
]


