from django.shortcuts import render, redirect, get_object_or_404 
from accounts.decorators import role_required
from datetime import date
from .models import SchemeCustomer, Deposit, DepositReceipt
from .forms import SchemeCustomerForm, DepositForm, PickupForm

# Create your views here.

# SCHEME CUSTOMER VIEWS

@role_required('accounts')
def customer_list(request):
# Get all registered scheme customers
    customers = SchemeCustomer.objects.all().order_by('-registered_at')
    return render(request, 'scheme/customer_list.html', {'customers': customers})


@role_required('accounts')
def customer_add(request):
    if request.method == 'POST':
        form = SchemeCustomerForm(request.POST)
        if form.is_valid():
            # Don't save yet — we need to add registered_by
            customer = form.save(commit=False)
            customer.registered_by = request.user
            customer.save()
            return redirect('scheme_customer_list')
    else:
        form = SchemeCustomerForm()

    return render(request, 'scheme/customer_form.html', {
        'form' : form,
        'title': 'Register Scheme Customer',
    })


@role_required('accounts')
def customer_detail(request, pk):
# Get one scheme customer and all their deposits
    customer = get_object_or_404(SchemeCustomer, pk=pk)
    deposits = customer.deposits.all().order_by('-deposit_date')
    return render(request, 'scheme/customer_detail.html', {
        'customer': customer,
        'deposits': deposits,
    })


# DEPOSIT VIEWS

@role_required('accounts')
def deposit_add(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
# Don't save yet — we need to add recorded_by
            deposit = form.save(commit=False)
            deposit.recorded_by = request.user
            deposit.save()

# Automatically generate a receipt number
# format: REC-00001, REC-00002 etc
            receipt_number = f"REC-{deposit.pk:05d}"

# Create the receipt and link it to this deposit
            DepositReceipt.objects.create(
                deposit        = deposit,
                receipt_number = receipt_number,
            )

# Redirect to the receipt page so customer gets their receipt
            return redirect('deposit_receipt', pk=deposit.pk)
    else:
        form = DepositForm()

    return render(request, 'scheme/deposit_form.html', {
        'form' : form,
        'title': 'Record Deposit',
    })


@role_required('accounts')
def deposit_receipt(request, pk):
    # Get the deposit and its receipt
    deposit = get_object_or_404(Deposit, pk=pk)
    receipt = deposit.receipt
    return render(request, 'scheme/receipt.html', {
        'deposit': deposit,
        'receipt': receipt,
    })


# PICKUP VIEW

@role_required('accounts')
def deposit_pickup(request, pk):
    # Get the deposit the customer wants to pick goods for
    deposit = get_object_or_404(Deposit, pk=pk)

    if request.method == 'POST':
        form = PickupForm(request.POST, instance=deposit)
        if form.is_valid():
# Don't save yet — we need to update status
            pickup = form.save(commit=False)
            pickup.status      = 'picked'  # mark as picked
            pickup.picked_date = date.today()  # set today as pickup date
            pickup.save()
            return redirect('scheme_customer_detail', pk=deposit.customer.pk)
    else:
        form = PickupForm(instance=deposit)

    return render(request, 'scheme/pickup_form.html', {
        'form'   : form,
        'deposit': deposit,
        'title'  : 'Record Goods Pickup',
    })

@role_required('accounts')
def customer_edit(request, pk):
    customer = get_object_or_404(SchemeCustomer, pk=pk)
    if request.method == 'POST':
        form = SchemeCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('scheme_customer_list')
    else:
        form = SchemeCustomerForm(instance=customer)
    return render(request, 'scheme/customer_form.html', {
        'form' : form,
        'title': 'Edit Scheme Customer',
    })