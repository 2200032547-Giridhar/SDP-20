from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm


urlpatterns = [
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('category/<slug:val>',CategoryView.as_view(),name='category'),
    path('category_title/<val>',CategoryTitle.as_view(),name='category_title'),
    path('book_detail/<int:pk>',BookDetail.as_view(),name='book_detail'),
    path('all-books/', AllBooksView.as_view(), name='all_books_view'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('address/', address, name='address'),
    path('updateaddress/<int:pk>',UpdateAddress.as_view(),name='updateaddress'),
    path('deleteaddress/<int:pk>',DeleteAddress.as_view(),name='deleteaddress'),
    path('paymentdone/',payment_done,name='paymentdone'),
    path('orders/',home,name='orders'),
    path('add_books/',add_book,name='add_books'),
    path('update_book/<int:pk>/', UpdateBook.as_view(), name='update_book'),
    path('delete_book/<int:pk>/', DeleteBook.as_view(), name='delete_book'),
    path('books/', BookListView.as_view(), name='books'),



    path('add_to_cart',add_to_cart,name='add_to_cart'),
    path('cart/',show_cart,name='showcart'),
    path('checkout/',checkout.as_view(),name='checkout'),


    path('pluscart/',plus_cart),
    path('minuscart/',minus_cart),
    path('removecart/',remove_cart),

                  #Login authentication
    path('registration/',CustomerRegistrationView.as_view(),name='customerragistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='change_password.html',form_class=MyPasswordChangeForm,success_url='/password_change_done'),name="password_change"),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
    path('logout/',Logout,name='logout'),
    path('adminHome',adminHome,name='adminHome'),
    path('login1/', Login1, name='login1'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done',auth_views.PasswordChangeDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)