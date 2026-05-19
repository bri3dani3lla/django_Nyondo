from django import forms
from .models import Sale, SaleItem, Customer 

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
        
class SaleForm(forms.ModelForm):
      # render payment_status as radio buttons not a dropdown
    payment_status = forms.ChoiceField(
        choices=Sale.PAYMENT_STATUS_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model  = Sale
        fields = [
            'customer',
            'within_10km',
            'payment_status',
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

