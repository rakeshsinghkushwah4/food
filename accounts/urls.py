"""FoodOrder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Singup/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name='logout'),

    path('home/',views.home,name="home"),
    path('product/',views.product,name="product"),
    path('customer/<int:pk>',views.customer,name="customer"),
    path('create_order/<int:pk>',views.createOrder,name="create_order"),
    path('update_order/<int:pk>',views.updateOrder,name="update_order"),
    path('delete_order/<int:pk>',views.deleteOrder,name="delete_order"),
    path('add_product/',views.addProduct,name='add_product'),
    path('edit_product/<slug:slug>',views.productEdit,name="edit_product"),
    path('search/<int:pk>',views.search,name='search'),
    path('ajax_test/',views.ajax_test,name='ajax_test'),
    path('cancel_product/<int:id>',views.Cancel_order,name='cancel_product'),


    path('user_page/',views.user,name='user_page'),
    path('accounts_settings/',views.accountsSettings,name='accounts_settings'),
    path('product_show/',views.Productshow,name='product_show'),
    path('order_product/<slug:slug>/<int:quntity>',views.order_customer,name='order_product'),
    path('product_details/<slug:slug>',views.productDetail,name='product_detail'),
    path('add_to_card/',views.add_to_card,name='add_to_card'),
    path('access_card/',views.access_card,name='access_card'),
    path('cancel_add_card/<int:id>/',views.cancel_add_card,name='cancel_add_card'),
    # path('create_session/',views.create_session),
    # path('access_session/',views.access_session),
    # path('delete_session/',views.delete_session),

    # Url for reset password 
    # Submit email url 
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='reset_password/reset_page.html'),
    name='reset_password'),
      # Email  send success m essage url
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_sent.html'),
    name='password_reset_done'),
    # Link to password Reset form in email
    path('reset_password/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/reset_password_form.html'),
    name='password_reset_confirm'),  
    # Passwrod successfully changed message
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/reset_password_done.html'),
    name='password_reset_complete'),

    path('simple_node/<str:strs>/',views.simple_node),
    path('',RedirectView.as_view(url='home/')),]
# ]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
