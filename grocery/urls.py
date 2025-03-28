

from django.urls import path
from .import views


urlpatterns = [
    path('', views.home,name='mainpage'),
    path('categories/<int:id>',views.category),
    path('productdetails/<int:id>',views.showproductdetails),
    path('addtocart',views.addtocart),
    path('loginuser',views.loginuser,name='loginuser'),
    path('signupuser',views.signupuser),
    path('logoutuser',views.logoutuser),
    path('cart',views.showcart),
    path('deleteitem',views.deletecart),
    path('updateitem',views.updatecart),
    path('checkout',views.checkout),
    path('complete_payment',views.complete_payment),
    path('myorders',views.myorders)
    
]
