from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sso_signin', views.sso_sign_in, name='sso_signin'),
    path('callback', views.sso_callback, name='sso_callback'),
    path('currentuser', views.currentuser, name='currentuser'),
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),

]