from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Sale, SaleItem, Customer 
from .forms import SaleForm, SaleItemForm, CustomerForm 
from datetime import date 

# Create your views here.

# CUSTOMER VIEWS

@login_required
def customer_list(request):
# Get all customers from the database
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})


@login_required
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form, 'title': 'Add Customer'})


# SALE VIEWS

@login_required
def sale_list(request):
# Get all sales, newest first
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'sales/sale_list.html', {'sales': sales})


@login_required
def sale_add(request):
    if request.method == 'POST':
        form     = SaleForm(request.POST)
        itemform = SaleItemForm(request.POST)

        if form.is_valid() and itemform.is_valid():
# Save the sale but don't commit yet
            sale          = form.save(commit=False)
            sale.sale_date = date.today()
            sale.served_by = request.user

# Save sale first so we can attach items to it
            sale.save()

# Save the sale item but don't commit yet
            item      = itemform.save(commit=False)
            item.sale = sale  # link the item to the sale
            item.save()

# Transport Calculation
# Now that the item is saved we can calculate the goods total
            goods_total = sale.goods_total()

            if sale.within_10km:
                if goods_total >= 500000:
        # Free delivery
                    sale.transport_fee    = 0
                    sale.transport_status = 'free'
                else:
        # Charge 30,000 UGX
                    sale.transport_fee    = 30000
                    sale.transport_status = 'charged'
            else:
        # Beyond 10km — no delivery
                sale.transport_fee    = 0
                sale.transport_status = 'none'

        # Update the product quantity in stock
            item.product.quantity_in_stock -= item.quantity
            item.product.save()

        # Save the sale again with transport details
            sale.save()

            return redirect('sale_list')
    else:
        form     = SaleForm()
        itemform = SaleItemForm()

    return render(request, 'sales/sale_form.html', {
        'form'    : form,
        'itemform': itemform,
        'title'   : 'Record Sale',
    })


@login_required
def sale_detail(request, pk):
# Get one sale and all its items
    sale  = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    return render(request, 'sales/sale_detail.html', {
        'sale' : sale,
        'items': items,
    })


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == 'POST':
# Reverse the quantity for each item in the sale
        for item in sale.items.all():
            item.product.quantity_in_stock += item.quantity
            item.product.save()
        sale.delete()
        return redirect('sale_list')

    return render(request, 'sales/confirm_delete.html', {'object': sale, 'type': 'Sale'})