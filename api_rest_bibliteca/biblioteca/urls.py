from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'autores',views.AutorViewSet)
router.register(r'libros',views.LibroViewSet)
router.register(r'prestamos',views.prestamoViewSet,basename='prestamos')

urlpatterns = [
    path('', include(router.urls)),         # root endpoints (/autores/, /libros/, /prestamos/)
    path('api/', include(router.urls)),      # optional prefix as before
]