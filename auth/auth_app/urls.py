from django.urls import path,include
from . import views 
from . import login

urlpatterns = [
    path('',login.login,name='login'),
    path('redirect/', views.redirect_to_42, name='redirect_to_42'),
    path('auth/callback/', views.callback, name='callback'),
    path('game/', login.game, name='game'),
    path('logout/',login.logout,name='logout'),
    path('profile/',login.profile,name='profile'),
    path('exit/',login.exit,name='exit'),
    # path('upload/', views.upload, name='upload'),
]