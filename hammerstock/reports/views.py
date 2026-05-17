from django.shortcuts import render
from accounts.decorators import role_required 
from stock.models import Product, StockEntry, Supplier
from sales.models import Sale, SaleItem
from scheme.models import SchemeCustomer, Deposit 

# Create your views here.
@role_required('accounts')
def reports_dashboard(request):
    # ── Stock summary ──
    # total number of products
    total_products = Product.objects.count()
    # products that are out of stock
    out_of_stock   = Product.objects.filter(quantity_in_stock=0).count()

    # ── Sales summary ──
    all_sales      = Sale.objects.all()
    total_sales    = all_sales.count()
    # add up all grand totals across all sales
    total_revenue  = sum(sale.grand_total() for sale in all_sales)

    # ── Supplier credit summary ──
    # suppliers who are owed money
    suppliers_on_credit = Supplier.objects.filter(credit_balance__gt=0)

    # ── Scheme summary ──
    total_scheme_customers = SchemeCustomer.objects.count()
    pending_deposits       = Deposit.objects.filter(status='pending').count()
    picked_deposits        = Deposit.objects.filter(status='picked').count()

    return render(request, 'reports/dashboard.html', {
        'total_products'        : total_products,
        'out_of_stock'          : out_of_stock,
        'total_sales'           : total_sales,
        'total_revenue'         : total_revenue,
        'suppliers_on_credit'   : suppliers_on_credit,
        'total_scheme_customers': total_scheme_customers,
        'pending_deposits'      : pending_deposits,
        'picked_deposits'       : picked_deposits,
    })


@role_required('accounts')
def stock_report(request):
    # All products with their current stock levels
    products = Product.objects.all().order_by('category')
    return render(request, 'reports/stock_report.html', {'products': products})


@role_required('accounts')
def sales_report(request):
    # All sales with totals
    sales         = Sale.objects.all().order_by('-sale_date')
    total_revenue = sum(sale.grand_total() for sale in sales)
    return render(request, 'reports/sales_report.html', {
        'sales'        : sales,
        'total_revenue': total_revenue,
    })


@role_required('accounts')
def scheme_report(request):
    # All scheme customers with their deposit totals
    customers = SchemeCustomer.objects.all()
    return render(request, 'reports/scheme_report.html', {'customers': customers})