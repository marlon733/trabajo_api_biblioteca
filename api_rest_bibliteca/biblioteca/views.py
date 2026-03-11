
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Autor,libro,prestamo
from .serializers import AutorSerializer,LibroSerializer,prestamoSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidad']
    search_fields = ['nombre','apellido']
    ordering_fields = ['nombre','fecha_nacimiento']
    ordering = ['nombre','apellido']
    
    
    
    
class LibroViewSet(viewsets.ModelViewSet):
    queryset = libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genero','disponible','autor']
    search_fields = ['titulo',"autor__nombre","autor__apellido"]
    # use the actual model field name (currently fecha_nacimiento)
    ordering_fields = ['titulo','fecha_nacimiento']
    ordering = ['fecha_nacimiento']
    
    # list action rather than detail; returning all available books
    @action(detail=False, methods=['get'])
    def disponible(self, request):
        libro_disponobles = self.queryset.filter(disponible=True)
        serializer = self.get_serializer(libro_disponobles, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True,methods=['post'])
    def prestar(self,request,pk=None):
        libro = self.get_object()
        if not libro.disponible:
            return Response({"error":"El libro no está disponible"},status=status.HTTP_400_BAD_REQUEST)
        
        prestamo = prestamo.objects.create(libro=libro,usuario=request.user)
        libro.disponible = False
        libro.save()
        return Response({"message": f"El libro {libro.titulo} ha sido prestado a {request.user.username}"},status=status.HTTP_200_OK)
class prestamoViewSet(viewsets.ModelViewSet):
    serializer_class = prestamoSerializer
    permission_classes = [IsAuthenticated]           # require authentication for all operations
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['devuelto','usuario']
    ordering = ['fecha_prestamo']

    def get_queryset(self):
        # if user is not authenticated, return empty queryset to avoid filtering on AnonymousUser
        if not self.request.user or not self.request.user.is_authenticated:
            return prestamo.objects.none()
        if self.request.user.is_staff:
            return prestamo.objects.all()
        return prestamo.objects.filter(usuario=self.request.user)
    
    @action(detail=True,methods=['post'])
    def devolver(self,request,pk=None):
        prestamo = self.get_object()
        if prestamo.devuelto:
            return Response({"error":"El libro ya ha sido devuelto"},status=status.HTTP_400_BAD_REQUEST)
        prestamo.devuelto = True
        prestamo.save()
        prestamo.libro.disponible = True
        prestamo.libro.save()
        return Response({"message":f"El libro {prestamo.libro.titulo} ha sido devuelto"},status=status.HTTP_200_OK)
# Create your views here.
