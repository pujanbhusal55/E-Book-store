

from django.contrib import admin
from .models import *



admin.site.register(Book)

admin.site.register(Cart)

admin.site.register(CartItem)

admin.site.register(WishlistItem)

admin.site.register(BookOrder)

admin.site.register(BookPaid)

admin.site.register(BookUrl)