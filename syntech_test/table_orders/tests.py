from django.test import TestCase
from .models import Table, Order, Hall
from .validators import username_validator
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Create your tests here.
class ValidatorsTestCase(TestCase):
    def setUp(self):
        pass


class OrdersTestCase(TestCase):

    def setUp(self):
        hall = Hall.objects.create(name = "Test hall", width = 200.0, depth = 500.0)
        table = Table.objects.create(hall=hall, number = 0, is_round = 1, seats_count = 10, x = 10, y = 10, width = 200, height = 200)
        Order.objects.create(table=table, date = now(),  mail="example@example.com" )

    def test_cascade_deletion(self):
        hall = Hall.objects.get(name = "Test hall")

        hall.delete()

    # There must be a better way. TODO: Google dat shit

        try:
            Table.objects.get(number=0)
        except Table.DoesNotExist:
            pass

        try:
            Order.objects.get(mail = "example@example.com")
        except Order.DoesNotExist:
            pass
