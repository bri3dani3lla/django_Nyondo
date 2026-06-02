from django import forms
from .models import Sale, SaleItem, Customer 

class CustomerForm(forms.ModelForm):
    class Meta:
        model  = Customer
        fields = ['name', 'phone', 'address']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # phone is optional on customer — only validate if provided
        if not phone:
            return phone

        phone = phone.replace(' ', '')

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

