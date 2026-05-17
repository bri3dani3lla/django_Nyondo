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

    def clean_full_name(self):
        """
        Full name must match national ID exactly.
        At least two names required.
        """
        full_name = self.cleaned_data['full_name']
        parts     = full_name.strip().split()
        if len(parts) < 2:
            raise forms.ValidationError(
                'Please enter your full name as it appears on your National ID. '
                'At least two names are required.'
            )
        return full_name.strip()

    def clean_nin(self):
        """
        Uganda NIN format: CM followed by 12 alphanumeric characters.
        Total length: 14 characters.
        Example: CM92760340TD8A
        """
        nin = self.cleaned_data['nin'].strip().upper()

        if len(nin) != 14:
            raise forms.ValidationError(
                'NIN must be exactly 14 characters e.g. CM92760340TD8A.'
            )
        if not (nin.startswith('CM') or nin.startswith('CF')):
            raise forms.ValidationError(
                'NIN must start with CM (male) or CF (female).'
            )
        if not nin[2:].isalnum():
            raise forms.ValidationError(
                'NIN must contain only letters and numbers after CM/CF.'
            )
        return nin

    def clean_phone(self):
        """
        Valid Ugandan phone number.
        Formats: 07XXXXXXXX or 03XXXXXXXX or +256XXXXXXXXX
        """
        phone = self.cleaned_data['phone'].replace(' ', '')

        if phone.startswith('+256'):
            number = phone[4:]
            if not number.isdigit():
                raise forms.ValidationError('Phone number must contain digits only.')
            if len(number) != 9:
                raise forms.ValidationError('Invalid Ugandan phone number.')
            if not (number.startswith('7') or number.startswith('3')):
                raise forms.ValidationError('Invalid Ugandan phone number.')
        elif phone.startswith('0'):
            if not phone.isdigit():
                raise forms.ValidationError('Phone number must contain digits only.')
            if len(phone) != 10:
                raise forms.ValidationError('Phone number must be 10 digits e.g. 0712345678.')
            if not (phone.startswith('07') or phone.startswith('03')):
                raise forms.ValidationError('Invalid Ugandan phone number. Must start with 07 or 03.')
        else:
            raise forms.ValidationError('Enter a valid Ugandan phone number e.g. 0712345678.')

        return phone


class DepositForm(forms.ModelForm):
    class Meta:
        model  = Deposit
        fields = [
            'customer',
            'product',
            'amount',
        ]

    def clean_amount(self):
        """
        Deposit amount must be greater than zero.
        """
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Deposit amount must be greater than zero.')
        return amount

    def clean_product(self):
        """
        Only cement, iron sheets and iron bars are allowed
        under the deposit scheme — as per the brief.
        """
        product = self.cleaned_data['product']
        allowed = ['cement', 'iron_bar', 'iron_sheet']

        if product.category not in allowed:
            raise forms.ValidationError(
                'Only Cement, Iron Bars and Iron Sheets are allowed '
                'under the deposit scheme.'
            )
        return product


class PickupForm(forms.ModelForm):
    class Meta:
        model  = Deposit
        fields = [
            'quantity_picked',
            'picked_date',
        ]

    def clean_quantity_picked(self):
        quantity = self.cleaned_data['quantity_picked']
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError('Quantity picked must be greater than zero.')
        return quantity