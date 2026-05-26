from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .models import Sale, Customer
from .forms import SaleForm, SaleItemForm, CustomerForm
from datetime import date


# CUSTOMER VIEWS

@role_required('attendant', 'manager')
def customer_list(request):
    # Get all customers from the database
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})


@role_required('attendant', 'manager')
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {
        'form' : form,
        'title': 'Add Customer',
    })


# SALE VIEWS

@role_required('attendant', 'manager')
def sale_list(request):
    # Get all sales, newest first
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'sales/sale_list.html', {'sales': sales})


@role_required('attendant', 'manager')
def sale_add(request):
    if request.method == 'POST':
        form     = SaleForm(request.POST)
        itemform = SaleItemForm(request.POST)

        if form.is_valid() and itemform.is_valid():
            # Save the sale but don't commit yet
            sale           = form.save(commit=False)
            sale.sale_date = date.today()
            sale.served_by = request.user
            # Save sale first so we can attach items to it
            sale.save()

            # Save the sale item but don't commit yet
            item      = itemform.save(commit=False)
            item.sale = sale  # link the item to the sale

            # Stock validation — check if enough stock exists
            if item.quantity > item.product.quantity_in_stock:
                # not enough stock — delete the sale and show error
                sale.delete()
                itemform.add_error(
                    'quantity',
                    f'Not enough stock. Only '
                    f'{item.product.quantity_in_stock} units available.'
                )
                return render(request, 'sales/sale_form.html', {
                    'form'    : form,
                    'itemform': itemform,
                    'title'   : 'Record Sale',
                })

            item.save()

            # Transport calculation
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

            return redirect('sale_receipt', pk=sale.pk)

    else:
        form     = SaleForm()
        itemform = SaleItemForm()

    return render(request, 'sales/sale_form.html', {
        'form'    : form,
        'itemform': itemform,
        'title'   : 'Record Sale',
    })


@role_required('attendant', 'manager')
def sale_receipt(request, pk):
    # Get one sale and all its items
    sale  = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    return render(request, 'sales/sale_receipt.html', {
        'sale' : sale,
        'items': items,
    })


@role_required('attendant', 'manager')
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        # Reverse the quantity for each item in the sale
        for item in sale.items.all():
            item.product.quantity_in_stock += item.quantity
            item.product.save()
        sale.delete()
        return redirect('sale_list')
    return render(request, 'sales/confirm_delete.html', {
        'object': sale,
        'type'  : 'Sale',
    })


@role_required('attendant', 'manager')
def sales_dashboard(request):
    # Recent sales — last 5
    recent_sales  = Sale.objects.all().order_by('-sale_date')[:5]
    # Total sales count
    total_sales   = Sale.objects.all().count()
    # Total revenue
    all_sales     = Sale.objects.all()
    total_revenue = sum(sale.grand_total() for sale in all_sales)
    total_customers = Customer.objects.count()

    return render(request, 'sales/dashboard.html', {
        'recent_sales' : recent_sales,
        'total_sales'  : total_sales,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
    })