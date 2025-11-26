from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestao_financeira.views import registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestao_financeira.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('registro/', registro, name='registro'),
]
