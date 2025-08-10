from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from MemoryGameMVC import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Raíz: redirige a /home/
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),

    # Rutas de la app
    path('home/', app_views.home, name='home')
    ,
    path('historial/', app_views.history, name='history'),
    path('api/save-result/', app_views.save_result, name='save_result'),
    path('perfil/', app_views.profile, name='profile'),
    path('login/', app_views.login_view, name='login'),
    path('logout/', app_views.logout_view, name='logout'),
    path('registro/', app_views.registro_view, name='registro'),
]
