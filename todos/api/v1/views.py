from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from ...models import Todo
from .permissions import IsOwnerOrReadOnly
import requests
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
# ________________________________________________


class TodoListApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer
    queryset = Todo.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_201_CREATED)


# ________________________________________________


class TodoDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TodoSerializer
    queryset = Todo.objects.filter(is_active=True)
    lookup_field = 'pk'
    lookup_url_kwarg = 'todo-details'

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        return obj

    def get(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_object())
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_object(), data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        ser_data = self.get_serializer(
            instance=self.get_object(), data=request.data, partial=True
        )
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


# ________________________________________________

# Weather Api
# ===========

@api_view(['GET'])
@cache_page(key_prefix='weather_tehran',timeout=60*20)
def get_weathermap(request):
    """ getting weather api at Tehran City """
    
    params = {'q':'Tehran','lang':'fa','appid':'4a8e6acb730d122b707e6bb73b7c1cfb'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?',params)
    
    if response.status_code == 200:
        data = response.json()
        return Response(data=data,status=status.HTTP_200_OK)
    return Response(data={'details':'page is not Found'},status=status.HTTP_404_NOT_FOUND)
# ________________________________________________
