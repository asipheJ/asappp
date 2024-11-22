from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
]
