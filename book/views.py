from django.contrib.auth import logout
from django.db.models import Count, Q
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from .models import Book, Cart, Customer, Payment, OrderPlaced
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


class AllBooksView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'all_books.html', {'books': books})

class BookListView(View):

    def get(self, request):
        books = Book.objects.all()
        return render(request, 'all_books1.html', {'books': books})




class CategoryView(View):
    def get(self, request, val):
        book = Book.objects.filter(category=val)
        title = Book.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())


class CategoryTitle(View):
    def get(self, request, val):
        book = Book.objects.filter(title=val)
        title = Book.objects.filter(category=book[0].category).values('title')
        return render(request, 'category.html', locals())


class BookDetail(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        return render(request, 'bookdetail.html', locals())


class CustomerRegistrationView(View):
    def get(self, request):
        forms = CustomerRegistrationForm()
        return render(request, 'customerregistrtion.html', locals())

    def post(self, request):
        forms = CustomerRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Congratiulations! User Register Successfully")
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'customerregistrtion.html', locals())


class ProfileView(View):
    def get(self, request):
        forms = CustomerProfileForm()
        return render(request, 'profile.html', locals())

    def post(self, request):
        forms = CustomerProfileForm(request.POST)
        if forms.is_valid():
            user = request.user
            name = forms.cleaned_data['name']
            locality = forms.cleaned_data['locality']
            city = forms.cleaned_data['city']
            mobile = forms.cleaned_data['mobile']
            state = forms.cleaned_data['state']
            pincode = forms.cleaned_data['pincode']

            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state,
                           pincode=pincode)
            reg.save()

            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())


class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        forms = CustomerProfileForm(instance=add)
        return render(request, 'updateaddress.html', locals())

    def post(self, request, pk):
        forms = CustomerProfileForm(request.POST)
        if forms.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = forms.cleaned_data['name']
            add.locality = forms.cleaned_data['locality']
            add.city = forms.cleaned_data['city']
            add.mobile = forms.cleaned_data['mobile']
            add.state = forms.cleaned_data['state']
            add.pincode = forms.cleaned_data['pincode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

class DeleteAddress(View):
    def get(self, request, pk):
        try:
            address = Customer.objects.get(pk=pk)
            address.delete()
            messages.success(request, "Address Deleted Successfully")
        except Customer.DoesNotExist:
            messages.warning(request, "Address does not exist")

        return redirect('address')


def Logout(request):
    logout(request)
    return redirect('login')


def add_to_cart(request):
    user = request.user
    book_id = request.GET.get('book_id')
    book = Book.objects.get(id=book_id)
    Cart(user=user, book=book).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.book.discount_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'addtocart.html', locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.book.discount_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()
        return render(request, 'checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = get_object_or_404(Customer, id=cust_id)
    payment = get_object_or_404(Payment, razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, book=c.book, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")


def plus_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.book.discount_price for item in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.book.discount_price for item in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.book.discount_price for item in cart)
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_books')  # Redirect to the book list view after adding a book
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

class UpdateBook(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'update_book.html', {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Book Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect('books')

class DeleteBook(View):
    def get(self, request, pk):
        try:
            book = get_object_or_404(Book, pk=pk)
            book.delete()
            messages.success(request, "Book Deleted Successfully")
        except Book.DoesNotExist:
            messages.warning(request, "Book does not exist")

        return redirect('books')



def adminHome(request):
    return render(request,'adminhomepage.html')

from django.contrib.auth import authenticate, login

def Login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if len(username) >= 5:
                return redirect('profile')
            elif len(username) == 4:
                return redirect('adminHome')
            else:
                return redirect('accounts/login/')
        else:
            messages.info(request, 'Invalid Credentials.')
            return render(request, 'customerregistrtion.html')
    else:
        return render(request, 'customerregistrtion.html')

