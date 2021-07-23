from django.contrib import auth
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm
urlpatterns = [
    path('',views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

   
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path("maps/", views.maps),
    
    
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    
    path('vegetables/', views.vegetables, name='vegetables'),
    path('fruits/', views.fruits, name='fruits'),
    path('leafyherbs/', views.leafyherbs, name='leafyherbs'),


    path('product-detail/addratings/', views.addrating, name='rating'),
    

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name="login"),
    path('registration/',views.CustomerRegistrationView.as_view(), name='registration'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name="passwordchange"),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name="passwordchangedone"),
   
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    
    #reset password urls 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_done.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
