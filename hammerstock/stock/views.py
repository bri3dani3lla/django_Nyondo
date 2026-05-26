from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required 
from .models import Product, Supplier, StockEntry 
from .forms import ProductForm, SupplierForm, StockEntryForm

# we import both our classes from models.py & forms.py

# render takes a request, a template, and data to send to that template
# redirect sends the user to another page a form is saved
# get_object_or_404- fetches one record by its pk(primary key/ID), shows a 404 page if not found 
# request.method =='POST' - checks if the user submitted a form
# form.save(commit=False) - creates object but holds it in memory without saving to DB yet, so we can add extra fields like:registered_by


# Create your views here. 
@role_required('manager', 'attendant')
def stock_dashboard(request):
    products      = Product.objects.all()
    entries       = StockEntry.objects.all().order_by('-date_received')
    low_stock     = Product.objects.filter(
                        quantity_in_stock__gt=0,
                        quantity_in_stock__lt=10).count()
    out_of_stock  = Product.objects.filter(quantity_in_stock__lte=0).count()
    total_suppliers = Supplier.objects.count()

    return render(request, 'stock/dashboard.html', {
        'products'        : products,
        'entries'         : entries,
        'low_stock'       : low_stock,
        'out_of_stock'    : out_of_stock,
        'total_suppliers' : total_suppliers,
    })

# PDT VIEWS
@role_required('manager', 'attendant')
def product_list(request):
    # We fetch all pdts from the DB
    products = Product.objects.all() 
    return render(request, 'stock/product_list.html', {'products': products})

@role_required('manager')
def product_add(request):
# If the form was submitted (POST), process it
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # save the new product to the database
            return redirect('product_list')  # go back to product list

# If just opening the page (GET), show an empty form
    else:
        form = ProductForm()

    return render(request, 'stock/product_form.html', {'form': form, 'title': 'Add Product'})

@role_required('manager')
def product_edit(request, pk):
# Get the product we want to edit, or show 404 if it doesn't exist
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
# Fill the form with submitted data & the existing product instance
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
# Pre-fill the form with the existing product data
        form = ProductForm(instance=product)

    return render(request, 'stock/product_form.html', {'form': form, 'title': 'Edit Product'})


# SUPPLIER VIEWS
@role_required('manager')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'stock/supplier_list.html', {'suppliers': suppliers})

@role_required('manager')
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'stock/supplier_form.html', {'form': form, 'title': 'Add Supplier'})

@role_required('manager')
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'stock/supplier_form.html', {'form': form, 'title': 'Edit Supplier'})
  


# STOCK ENTRY VIEWS
@role_required('manager', 'attendant')
def stock_entry_list(request):
# Get all stock entries, newest first
    entries = StockEntry.objects.all().order_by('-date_received')
    return render(request, 'stock/stock_entry_list.html', {'entries': entries})

@role_required('manager')
def stock_entry_add(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            if request.user.is_authenticated:
                entry.registered_by = request.user
            # update product quantity
            entry.product.quantity_in_stock += entry.quantity
            entry.product.save()
            entry.save()

            # if payment is credit update supplier credit balance
            if entry.payment_type == 'credit':
                entry.supplier.credit_balance += entry.total_cost()
                entry.supplier.save()

            return redirect('stock_entry_list')
    else:
        form = StockEntryForm()
    return render(request, 'stock/stock_entry_form.html', {
        'form' : form,
        'title': 'Register Stock Entry',
    })


# DELETE VIEWS

@role_required('manager')
def product_delete(request, pk):
# Get the product we want to delete or show 404 if it doesn't exist
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
# If the user confirmed deletion, delete it
        product.delete()
        return redirect('product_list')

# If GET request, show a confirmation page first
# We never delete directly without asking the user to confirm
    return render(request, 'stock/confirm_delete.html', {'object': product, 'type': 'Product'})


@role_required('manager')
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')

    return render(request, 'stock/confirm_delete.html', {'object': supplier, 'type': 'Supplier'})


@role_required('manager')
def stock_entry_delete(request, pk):
    entry = get_object_or_404(StockEntry, pk=pk)

    if request.method == 'POST':
# Before deleting, reverse the quantity that was added to the product
        entry.product.quantity_in_stock -= entry.quantity
        entry.product.save()
        entry.delete()
        return redirect('stock_entry_list')

    return render(request, 'stock/confirm_delete.html', {'object': entry, 'type': 'Stock Entry'}) 
