from django.db import models




from django.utils import timezone
from django.contrib.auth.models import User

class Book(models.Model):
    bookID = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.FloatField()
    genres = models.CharField(max_length=200)
    characters = models.CharField(max_length=200)
    numRatings = models.IntegerField()
    coverImg = models.URLField(max_length=200)
    price = models.FloatField()
    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    check_out = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,  null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in {self.cart.user.username}'s Cart"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.wishlist.user.username}'s wishlist"
    

class BookOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_by = models.CharField(max_length=200)
    payment_completed = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    



class BookPaid(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Paid Book: {self.book.title} ({self.user.username})"

    
class BookUrl(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.book.title 