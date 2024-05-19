from django.db import models

class CryptoData(models.Model):
    symbol = models.CharField(max_length=10)

    open_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    high_price = models.DecimalField(max_digits=15, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2,default= 0.0)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.timestamp}"
