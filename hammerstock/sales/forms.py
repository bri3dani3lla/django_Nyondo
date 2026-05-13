from django import forms
from .models import Sale, SaleItem, Customer 

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
        
class SaleForm(forms.ModelForm):
    class Meta:
        model  = Sale
        fields = [
            'customer',
            'within_10km',
        ]
# We leave out transport_fee and transport_status
# because those will be calculated automatically
# in the view based on the goods total and within_10km
# sale_date is not here, it sets itself automatically

class SaleItemForm(forms.ModelForm):
    class Meta:
        model  = SaleItem
        fields = [
            'product',
            'quantity',
            'unit_price',
        ]        

