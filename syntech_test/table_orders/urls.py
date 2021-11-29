from django.urls import include, path
from rest_framework import routers

from . import views
from .models import Order
from .views import HallViewSet, OrderViewSet, TableViewSet

router = routers.DefaultRouter()


router.register(r'orders', OrderViewSet )
router.register(r'halls', HallViewSet)

router.register(r'table', TableViewSet)
urlpatterns = [
    path('', include(router.urls)),

    # path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
