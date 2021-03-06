"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    
    path('user/', views.userPage, name="user"),
    path('registration/', views.registrationPage, name="registration"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('new_user_info/', views.newUserInfo, name="new_user_info"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="store/reset_password.html"),
     name="reset_password"),
    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="store/reset_password_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"),
	 name="password_reset_confirm"),

    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
      name="password_reset_complete"),
    
    

]

""" path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="store/reset_password.html"),
     name="reset_password"),
    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="store/reset_password_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
      name="password_reset_complete"),
"""