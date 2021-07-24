from django.urls import path

from usuario import views


app_name = 'usuario'

urlpatterns = [
    path('criar/', views.CriarUsuarioView.as_view(), name='criar'),
    path('token/', views.CriarTokenView.as_view(), name='token'),
    path('eu/', views.GerenciarUsuarioView.as_view(), name='eu'),
]
