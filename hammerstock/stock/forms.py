from django import forms
from .models import Product, Supplier, StockEntry


class SupplierForm(forms.ModelForm):
    class Meta:
        model  = Supplier
        fields = ['name', 'phone',
                   'address', 'credit_balance',
                   'product_delivered', 'due_date',]

    def clean_phone(self):
        """
        Validate Ugandan phone number.
        Valid formats: 07XXXXXXXX (10 digits)
        or +2567XXXXXXXX or +2563XXXXXXXX (with country code)
        """
        phone = self.cleaned_data['phone']
        # remove spaces
        phone = phone.replace(' ', '')

        if phone.startswith('+256'):
            # international format +256XXXXXXXXX
            number = phone[4:]  # remove +256
            if not number.isdigit():
                raise forms.ValidationError('Phone number must contain digits only.')
            if len(number) != 9:
                raise forms.ValidationError('Invalid Ugandan phone number.')
            if not (number.startswith('7') or number.startswith('3')):
                raise forms.ValidationError('Invalid Ugandan phone number.')
        elif phone.startswith('0'):
            # local format 07XXXXXXXX
            if not phone.isdigit():
                raise forms.ValidationError('Phone number must contain digits only.')
            if len(phone) != 10:
                raise forms.ValidationError('Phone number must be 10 digits e.g. 0712345678.')
            if not (phone.startswith('07') or phone.startswith('03')):
                raise forms.ValidationError('Invalid Ugandan phone number. Must start with 07 or 03.')
        else:
            raise forms.ValidationError('Enter a valid Ugandan phone number e.g. 0712345678.')

        return phone


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'category', 'unit', 'description']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError('Product name must be at least 2 characters.')
        return name


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
            'storage_location',
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity

    def clean_unit_cost(self):
        unit_cost = self.cleaned_data['unit_cost']
        if unit_cost <= 0:
            raise forms.ValidationError('Unit cost must be greater than zero.')
        return unit_cost

    def clean(self):
        """
        clean() is used when we need to validate TWO fields together.
        Here we check that selling price is greater than cost price.
        This is explicitly required in the brief.
        """
        cleaned_data       = super().clean()
        unit_cost          = cleaned_data.get('unit_cost')
        unit_selling_price = cleaned_data.get('unit_selling_price')

        if unit_cost and unit_selling_price:
            if unit_selling_price <= unit_cost:
                raise forms.ValidationError(
                    'Selling price must be greater than cost price. '
                    f'Cost is {unit_cost} — selling price must be higher.'
                )
        return cleaned_data