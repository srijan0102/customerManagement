from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views

# Wthout app_name : Exception ImproperlyConfigured : Specifying a namespace in include() without providing an app_name is not supported. 
# Set the app_name attribute in the included module, or pass a 2-tuple containing the list of patterns and app_name instead.
app_name ='accounts' 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('register/', views.register, name='register'),
    
    path('products/', views.products, name='products'),
    path('profile/', views.account_profile, name='profile'),
    path('customer/', views.customer_profile, name="customer_profile"),
    path('customer/<str:pk>/', views.customer, name='customer'),
    
    path('create_order/<str:customer_pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    
    #Pasword Reset
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html",  
                                                                email_template_name = 'password_reset_email.html',
                                                                success_url = reverse_lazy('accounts:password_reset_done')),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html",
                                                                               success_url = reverse_lazy('accounts:password_reset_complete')),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html",), name="password_reset_complete"),

]
