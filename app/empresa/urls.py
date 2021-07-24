from django.urls import path, include
from rest_framework.routers import DefaultRouter

from empresa import views


router = DefaultRouter()
router.register('empresas', views.EmpresaViewSet)
router.register('motoristas', views.MotoristaViewSet)

app_name = 'empresa'

urlpatterns = [
    path('', include(router.urls))
]
