from django.db import models
from stock.models import Product

# Create your models here.
class Customer(models.Model):
    name    = models.CharField(max_length=200)
    phone   = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    TRANSPORT_CHOICES = [
        ('none',    'No delivery'),
        ('free',    'Free delivery'),
        ('charged', 'Charged 30,000 UGX'),
    ]

    customer         = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    sale_date        = models.DateField()
    within_10km      = models.BooleanField(default=False)
    transport_fee    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_status = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, default='none')
    served_by        = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='sales')
    created_at       = models.DateTimeField(auto_now_add=True)

    def goods_total(self):
# add up all line items in this sale
        return sum(item.line_total() for item in self.items.all())

    def grand_total(self):
# goods total plus transport fee
        return self.goods_total() + self.transport_fee

    def __str__(self):
        return f"Sale #{self.pk} on {self.sale_date}"


class SaleItem(models.Model):
# links each product line to its sale
    sale       = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    quantity   = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product} x {self.quantity}"     