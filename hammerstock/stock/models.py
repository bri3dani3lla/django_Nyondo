from django.db import models

# Create your models here.
# Supplier model 
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):

# categories available for products
    CATEGORY_CHOICES = [
        ('cement',      'Cement'),
        ('iron_bar',    'Iron Bar'),
        ('nail',        'Nail'),
        ('wheelbarrow', 'Wheelbarrow'),
        ('wire_mesh',   'Wire Mesh'),
        ('barbed_wire', 'Barbed Wire'),
        ('iron_sheet',  'Iron Sheet'),
    ]

# units used to measure products
    UNIT_CHOICES = [
        ('bag',   'Bag'),
        ('piece', 'Piece'),
        ('kg',    'Kilogram'),
        ('roll',  'Roll'),
        ('sheet', 'Sheet'),
    ]

    name              = models.CharField(max_length=200)
    category          = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    unit              = models.CharField(max_length=20, choices=UNIT_CHOICES)
    description       = models.CharField(max_length=255, blank=True)
    quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# display pdt name with its units
    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"

# StockEntry model
class StockEntry(models.Model):

    PAYMENT_CHOICES = [
        ('cash',   'Cash'),
        ('credit', 'Credit (pay later)'),
    ]

    product            = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_entries')
    supplier           = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='stock_entries')
    quantity           = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost          = models.DecimalField(max_digits=10, decimal_places=2)
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type       = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    amount_paid        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_received      = models.DateField()
    notes              = models.TextField(blank=True)
    registered_by      = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at         = models.DateTimeField(auto_now_add=True)

# Calculates total cost of stock
    def total_cost(self):
        return self.quantity * self.unit_cost
# Calculates remaining amount owed
    def amount_owed(self):
        return self.total_cost() - self.amount_paid
# String representation of stock entry 
    def __str__(self):
        return f"{self.product} - {self.quantity} units on {self.date_received}"

# ForeignKey to Product & Supplier; links this entry to which product arrived and from which supplier
# unit_cost vs unit_selling_price — cost is what Nyondo paid, selling price is what they charge customers
# payment_type — was it cash or credit (pay later)?
# amount_paid — if credit, how much has been paid so far
# registered_by — which user logged this stock entry 