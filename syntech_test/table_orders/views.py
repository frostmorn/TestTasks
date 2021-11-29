from django.shortcuts import render
from rest_framework import viewsets
from .models import Order, Hall, Table
from .serializers import OrderSerializer, HallSerializer, TableSerializer
from django.http.response import HttpResponse
from rest_framework.response import Response
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class HallViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving halls.
    """
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    

class TableViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving tables.
    """
    queryset = Table.objects.all()

    serializer_class = TableSerializer
        

