from django.contrib import admin

from .models import Hall
from .models import Table
from .models import Order

# Register your models here.

class TableAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hall, TableAdmin)

admin.site.register(Table, TableAdmin)

admin.site.register(Order, TableAdmin)