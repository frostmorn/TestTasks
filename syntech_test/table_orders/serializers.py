from .models import Order, Table, Hall
from rest_framework import routers, serializers
# Serializers define the API representation.



class HallSerializer(serializers.ModelSerializer):
    """
    A simple ViewSet for listing or retrieving halls.
    """
    class Meta:
        model = Hall
        fields = ["name", "width", "depth"]


class TableSerializer(serializers.ModelSerializer):
    """
    A simple ViewSet for listing or retrieving tables.
    """
    class Meta:
        model = Table
        fields = ["id","hall","number", "is_round", "x", "y","width", "height", "seats_count"]

class AvaliableTablesSerializer(serializers.ModelSerializer):
    """
    A simple ViewSet for listing or retrieving tables.
    """
    class Meta:
        model = Table
        fields = ["id","hall","number", "is_round", "x", "y","width", "height", "seats_count"]


class OrderSerializer(serializers.ModelSerializer):
    """
    A simple ViewSet for listing or retrieving orders.
    """
    class OrderSerializer(serializers.ModelSerializer):
        pass
    class Meta:
        model = Order
        fields = ["id", "date","tables", "mail", "username"]
    