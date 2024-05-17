from django.urls import path
from eco import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('pay/', views.pay, name='pay'),
    path('token/', views.token, name='token'),
    path('stk/', views.stk, name='stk')

]

