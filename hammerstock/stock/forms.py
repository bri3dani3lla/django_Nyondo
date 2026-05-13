from django import forms
from .models import Product, Supplier, StockEntry

# we import all our classes from models.py; Product, Supplier, StockEntry

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address'] 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'category', 'unit', 'description']

class StockEntryForm(forms.ModelForm):
    class Meta:
        model  = StockEntry
        fields = [
            'product',
            'supplier',
            'quantity',
            'unit_cost',
            'unit_selling_price',
            'payment_type',
            'amount_paid',
            'date_received',
            'notes',
        ] 