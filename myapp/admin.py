from django.contrib import admin
from .models import CryptoData

@admin.register(CryptoData)
class CryptoDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'open_price', 'high_price', 'low_price', 'close_price', 'timestamp')

# Register your models here.
