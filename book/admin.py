from django.contrib import admin
from .models import Book, Customer, Cart, Payment, OrderPlaced


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discount_price','category','book_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','pincode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','book','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','book','quantity','ordered_date','status','payment']