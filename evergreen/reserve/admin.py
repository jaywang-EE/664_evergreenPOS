from django.contrib import admin
from reserve.models import Reserve, Table, TableType

# Register your models here.

admin.site.register(Reserve)
admin.site.register(Table)
admin.site.register(TableType)

