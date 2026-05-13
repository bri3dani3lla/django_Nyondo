from django.db import models
from stock.models import Product

# Create your models here.
class SchemeCustomer(models.Model):
    """
    A salary earner registered for the deposit scheme.
    Only cement, iron sheets and iron bars are allowed.
    Full name must match the name on their national ID exactly.
    """
    full_name     = models.CharField(max_length=200)
    nin           = models.CharField(max_length=20, unique=True, verbose_name='NIN')
    phone         = models.CharField(max_length=20)
    occupation      = models.CharField(max_length=200, blank=True)
    address       = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, related_name='scheme_registrations'
    )

    def total_deposited(self):
        # add up all deposits this customer has made
        return sum(d.amount for d in self.deposits.all())

    def __str__(self):
        return f"{self.full_name} ({self.nin})"


class Deposit(models.Model):
    """
    One deposit payment made by a scheme customer.
    A receipt is automatically created for each deposit.
    When customer picks goods, status changes to picked.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending - goods not yet picked'),
        ('picked',  'Goods picked'),
    ]

    customer        = models.ForeignKey(SchemeCustomer, on_delete=models.PROTECT, related_name='deposits')
    product         = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='deposits')
    amount          = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_date    = models.DateField(auto_now_add=True)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    quantity_picked = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    picked_date     = models.DateField(null=True, blank=True)
    recorded_by     = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, related_name='deposits'
    )

    def __str__(self):
        return f"{self.customer} - {self.amount} UGX on {self.deposit_date}"
# f-string means anything inside{}is a variable - replace it with its value

class DepositReceipt(models.Model):
    """
    A temporary receipt issued every time a deposit is made.
    One receipt per deposit — OneToOneField.
    """
    deposit        = models.OneToOneField(Deposit, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=30, unique=True)
    issued_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receipt_number}"