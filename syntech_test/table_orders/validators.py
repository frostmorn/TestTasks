
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


usernameValidator = RegexValidator('[a-zA-Zа-яА-Я].{1,60}')

def table_order_validator(table):

    print("table type "+str(type(table)))
    raise ValidationError("Table validator failed")


def biggerThanZero(value):
    if value <= 0:
        raise ValidationError("Can't be lower or equal to zero")

def emptyValidator(data):

    pass

# M2M changed callback. Not a regular Validator
def validate_tableAvalibility(sender, **kwargs):
# Be sure that table is not allready reserved
    instance = kwargs.pop('instance', None)
    model = kwargs.pop('model', None)
    try:
        from .models import Order
    except ImportError:
        return

    orders_on_date = Order.objects.filter(date=instance.date)

    tables = model.objects.all()
    for order in orders_on_date:
        # Be sure that current id is not equall to order.
        if instance.id != order.id:
            for o_table in order.tables.all():
                for table in tables:
                    if table.id == o_table.id:
                        raise ValidationError("Table allready reserved. {table}, {date}".format(table=table, date = instance.date))
                        return

    instance.save()