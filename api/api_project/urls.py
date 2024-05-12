from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_app.urls')),

    # path('', include('chat_app.urls')),
    # path('',include('auth_app.urls')),
    # path('login/', include('auth_app.urls')), 
    # path('auth/callback/', include('auth_app.urls')),  
    # path('redirect/', include('auth_app.urls')),  
    # path('logout/', include('auth_app.urls')),
    # path('game/', include('auth_app.urls')),
]
