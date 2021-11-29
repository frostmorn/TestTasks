from django.db.models.signals import m2m_changed
from django.db import models
from django.core.validators import EmailValidator
from .validators import biggerThanZero, usernameValidator, validate_tableAvalibility
from .validators import emptyValidator


from django.core.exceptions import ValidationError

# Create your models here.
class Hall(models.Model):
    name = models.CharField(max_length=60, default = "Big Hall")
    width = models.FloatField(validators = [biggerThanZero])
    # We use depth there, cause height mostly associates with z axis
    depth = models.FloatField(validators = [biggerThanZero])
    
    def __str__(self):
        return "[ Hall: {hall_name} ]".format(hall_name = self.name)

class Table(models.Model):
    
    hall = models.OneToOneField(Hall, on_delete = models.CASCADE)
    number = models.PositiveIntegerField(validators = [biggerThanZero])

    # table form type
    is_round = models.BooleanField()

    # Location(Cords of table center inside hall):
    # by Hall width 
    x = models.FloatField(validators = [biggerThanZero]) 
    # by Hall depth
    y = models.FloatField(validators = [biggerThanZero])

    # x-axis
    width = models.FloatField(validators = [biggerThanZero])
    # y-axis
    height = models.FloatField(validators = [biggerThanZero])
    
    seats_count = models.PositiveSmallIntegerField(validators = [biggerThanZero])
    def validate_table_pos(self):
        # tables_in_current_hall = Table.objects.filter(hall=self.hall)
        # if tables_in_current_hall.exists():
        #     for table in tables_in_current_hall:
        #         if table.id != self.id:
        #             print(table, self)

                    
        pass

    def clean_fields(self, exclude=(is_round, seats_count)):
        
        # validate table location
        self.validate_table_pos()

    def __str__(self):
        return "[ Table: № {table_number} ]{hall_name}".format(table_number = self.number, hall_name = self.hall)

class Order(models.Model):

    date = models.DateField()
    tables = models.ManyToManyField(Table)
    mail = models.EmailField(null=True, validators=[EmailValidator()])
    # By default order isn't paid yet, so we expect it is reserved
    is_paid = models.BooleanField(default=False)
    username = models.CharField(max_length=60, validators=[usernameValidator], null=True)

    def validate_date_tables(self):

        all_orders = Order.objects.filter(date=self.date)
        # if self.id == null, we can't work with M2M fields
        if not all_orders.exists() or self.id == None:
            return
        self_order_tables = self.tables.all()

        # could be more beautifull implementation, but it works
        for order in all_orders:
            if order.id != self.id:
                order_tables = order.tables.all()
                for o_table in order_tables:
                    for s_table in self_order_tables:
                        if s_table == o_table:
                            raise ValidationError("Table {table} allready reserved on date {date}".format(table = s_table, date=self.date))
    
    def clean_fields(self, exclude=(mail,username)):
        # validate table reserved
        self.validate_date_tables()

    def __str__(self):
        return "[ Order: #{order_id}, {date} ]".format(order_id = self.id, date=self.date)

    

# Validate table avalibility on m2m signal 
# By default clean_fields method can't work with realationships 
# if object isn't allready saved to database -_-

m2m_changed.connect(validate_tableAvalibility, sender=Order.tables.through)


