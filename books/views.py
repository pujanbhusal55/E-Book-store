
from django.http import HttpResponseNotFound
from .models import Book
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def home(request):
    return render(request, 'users/home.html')

#def store(request):
 #   books = Book.objects.all()
 #   context = {
  #      'books': books
   # }
  #  return render(request, 'store.html', context)



from django.core.paginator import Paginator

@login_required
def store(request):
    book_list = Book.objects.all().order_by('bookID')  
    paginator = Paginator(book_list, 6)
    page_number = request.GET.get('page')

    books_page = paginator.get_page(page_number)

    # try:
    #     cart = Cart.objects.filter(user=request.user, check_out=False).get()
    #     item_count = CartItem.objects.filter(cart=cart).count()
    # except Cart.DoesNotExist:
    #     cart = None
    #     item_count = 0
    context = {
        'books': books_page,
       
    }

    return render(request, 'store.html', context)






from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book
    }
    return render(request, 'bookDetail.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem, WishlistItem, Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect



from django.core.exceptions import ObjectDoesNotExist

# def get_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user, check_out=False)
#     if cart.exists():
#         print("the cart does not exits")
#         return cart[0]
#     cart = Cart.objects.create(user = user)
#     print("we create a new cart")
#     return cart

    
# @login_required
# def addcart(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     cart = get_cart(request)
#     print(cart)
#     user= request.user
#     try:
        
#         book=BookPaid.objects.get(book=book, user=user)

       
#         if book.id:
#             messages.info(request, f'{book.title} is already in your cart.')
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     except:
#         pass
#     if cart.cartitem_set.filter(book=book).exists():
#         # Book already in cart
#         messages.info(request, f'{book.title} is already in your cart.')
        
#     else:
#         # Add book to cart
#         CartItem.objects.create(cart=cart, book=book)
#         messages.success(request, f'{book.title} has been added to your cart.')
#     return redirect(request.META.get('HTTP_REFERER', '/'))




# @login_required
# def removecart(request, id):
#     cart_item = get_object_or_404(CartItem, id=id)
#     cart_item.delete()
#     return redirect('cartdetails')





# @login_required
# def cartdetails(request):
#     cart = get_cart(request)
#     cart_items = cart.cartitem_set.all()
#     total = sum(item.book.price * item.quantity for item in cart_items)
    
#     cart = Cart.objects.filter(user = request.user)[0]
#     item_count = CartItem.objects.filter(cart = cart).count()
#     return render(request, 'cartDetail.html', {'cart_items': cart_items, 'total': total, 'items':item_count})



@login_required
def addwishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, book=book)
    if not created:
        messages.info(request, f"{book.title} is already in your wishlist.")
    else:
        messages.success(request, f"{book.title} is added to your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def removewishlist(request, id):
    wishlist_items = get_object_or_404(WishlistItem, id=id)
    wishlist_items.delete()
    return redirect('wishdetails')


@login_required
def wishdetails(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    #wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_items = wishlist.items.all()
    item_count = 0
    try:
        wishlist = Wishlist.objects.filter(user=request.user)[0]
        item_count = WishlistItem.objects.filter(wishlist=wishlist).count()
    except IndexError:
        pass
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'item_count': item_count})


'''
def profile(request):
    if request.user.is_authenticated:
        order, created = CartItem.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = [] 
    
    return render(request,'profile.html',{'items':items,'cartItems':cartItems})
'''



from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import scipy as sp
from .models import Book
from .forms import BookSearchForm

#features = [book.author + ' ' + book.description + ' ' + book.genres + ' ' + book.characters for book in books]



from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from nltk.corpus import stopwords

stopwords_english = stopwords.words('english')

books = Book.objects.all()

def preprocess_text(text):
    text = str(text)
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stopwords_english and t not in string.punctuation]
    return ' '.join(tokens)
    
def preprocess_books(books):
    for book in books:
        book.author_processed = preprocess_text(book.author)
        book.description_processed = preprocess_text(book.description)
        book.genres_processed = preprocess_text(book.genres)
        book.characters_processed = preprocess_text(book.characters)
        book.features = book.author_processed + ' ' + book.description_processed + ' ' + \
                        book.genres_processed + ' ' + book.characters_processed


preprocess_books(books)
features = vectorizer.fit_transform([book.features for book in books])
cosine_sim = cosine_similarity(features)


def recommend_books(title):
    
   
    book = Book.objects.get(title=title)

    
    idx = list(books).index(book)


    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books by similarity score in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 most similar books
    sim_scores = sim_scores[1:6]

    # Get the indices of the top 5 most similar books
    book_indices = [i[0] for i in sim_scores]

    # Return the bookID, titles, authors, cover images, and prices of the top 5 most similar books
    recommended_books = []
    for i in book_indices:
        book = books[i]
        recommended_book = {
            'bookID' : book.bookID,
            'title': book.title,
            'author': book.author,
            'coverImg': book.coverImg,
            'price': book.price
        }
        recommended_books.append(recommended_book)

    return recommended_books


def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        # Find books that match the query in the title, author
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        # If there are matching books, get recommendations based on the first book in the queryset
        if books:
            book = books.first()
            recommended_books = recommend_books(book.title)
            
        else:
            recommended_books = []
        return render(request, 'search.html', {'query': query, 'books': books, 'recommended_books': recommended_books})
    else:
        return render(request, 'search.html')




# @login_required
# def checkout(request):
#     cart = get_cart(request)
#     cart_items = cart.cartitem_set.all()
#     total = sum(item.book.price * item.quantity for item in cart_items)

#     if request.method == 'POST':
#         # messages.success(request, 'Your order has been placed successfully.')
#         return redirect('cartdetails')

#     return render(request, 'checkout.html', {'cart':cart, 'cart_items': cart_items, 'total': total})



from django.http import JsonResponse
import requests

def verify_payment(request):
    user = request.user
    print("this view activated")
    if request.method == "GET":
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        cartid = request.GET.get("cartid")
        url = "https://khalti.com/api/v2/payment/verify/"
        
        payload = {
                    'token': token,
                    'amount': amount
                }
        headers = {
            # add your own uthorization test secret key
            'Authorization': 
        }
        
        response = requests.post(url, payload, headers=headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            # returning the payment status
            success = True
            cart = Cart.objects.get(id = cartid)
            cart.check_out=True
            cart.save()
            books = cart.cartitem_set.all()
            
            for book in books:
                BookPaid.objects.create(user = request.user, book = book.book)
            
        else:
            success = False
        
        data = {
            'success' : success
        }
        
    return JsonResponse(data)


@login_required
def my_books(request):
    user = request.user
    books = BookPaid.objects.filter(user = user)
    
    mybooks = []
    for book in books:
        mybooks.append(BookUrl.objects.get(book = book.book))
    context = {
        'mybooks' : mybooks
    }
    #for book in mybooks:
     #   print(book.book.title, book.url)
    return render(request, 'mybooks.html', context)

'''
@login_required
def removepurchasedbook(request, id):
    print("id:", id)
    bookpdf_items = get_object_or_404(BookPaid, id=id)
    bookpdf_items.delete()
    return redirect('my_books')
'''

def buybook(request, id):
    cart= Cart.objects.create(user= request.user)
  
    book= get_object_or_404(Book, bookID=id)
    try:
        book=BookPaid.objects.get(book=book, user=request.user)
     
        if book.id:
            messages.info(request, "Book already in your inventory")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        pass
    cart_items= CartItem.objects.create(book=book, cart=cart)
    total = cart_items.quantity*book.price

    if request.method == 'POST':
        # messages.success(request, 'Your order has been placed successfully.')
        return redirect('cartdetails')

    return render(request, 'buyproduct.html', {'cart':cart, 'cart_items': cart_items, 'total': total})



# @login_required
# def userdelete(request):
#     if request.method == 'POST':
#         if 'delete_account' in request.POST:
#             user = request.user
#             user.delete()
#             message_delete = "Account deleted successfully."
#             messages.success(request, message_delete)  # Add this line to display the success message
#             return render(request, 'users-home.html')
#         elif 'cancel' in request.POST:
#             return redirect('users-profile')
#     return render(request, 'conformdeleteuser.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Delete the user account
        user.delete()
        # Redirect to a success page or any other page
        return redirect('users-home')