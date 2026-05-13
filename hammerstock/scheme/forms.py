# scheme/forms.py

from django import forms
from .models import SchemeCustomer, Deposit


class SchemeCustomerForm(forms.ModelForm):
    class Meta:
        model  = SchemeCustomer
        fields = [
            'full_name',
            'nin',
            'phone',
            'occupation',
            'address',
        ]


class DepositForm(forms.ModelForm):
    class Meta:
        model  = Deposit
        fields = [
            'customer',
            'product',
            'amount',
        ]
# deposit_date sets itself automatically
# status starts as pending automatically
# recorded_by is set in the view


class PickupForm(forms.ModelForm):
    """
    This form is used when a customer comes to pick their goods.
    We record how many units they are picking and the date.
    """
    class Meta:
        model  = Deposit
        fields = [
            'quantity_picked',
            'picked_date',
        ]