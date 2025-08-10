from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("historial/", views.history, name="history"),
    path("api/save-result/", views.save_result, name="save_result"),  # importante: nombre usado por {% url %}
    path("perfil/", views.profile, name="profile"),                   # NUEVO
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registro/", views.registro_view, name="registro"),
]
