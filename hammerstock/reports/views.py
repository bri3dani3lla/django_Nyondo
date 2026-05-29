from django.shortcuts import render
from accounts.decorators import role_required 
from stock.models import Product, StockEntry, Supplier
from sales.models import Sale, SaleItem
from scheme.models import SchemeCustomer, Deposit 
from django.db.models import Sum

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
    total_credit_owed   = Supplier.objects.aggregate(total=Sum('credit_balance'))['total'] or 0

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
        'total_credit_owed'     : total_credit_owed,
        'total_scheme_customers': total_scheme_customers,
        'pending_deposits'      : pending_deposits,
        'picked_deposits'       : picked_deposits,
    })


@role_required('accounts')
def stock_report(request):
    products     = Product.objects.all().order_by('category')
    total        = products.count()
    out_of_stock = products.filter(quantity_in_stock=0).count()
    low_stock    = products.filter(
                       quantity_in_stock__gt=0,
                       quantity_in_stock__lte=20).count()
    in_stock     = products.filter(quantity_in_stock__gt=20).count()

    return render(request, 'reports/stock_report.html', {
        'products'    : products,
        'total'       : total,
        'out_of_stock': out_of_stock,
        'low_stock'   : low_stock,
        'in_stock'    : in_stock,
    })


@role_required('accounts')
def sales_report(request):
    # All sales with totals and average sale value
    sales         = Sale.objects.all().order_by('-sale_date')
    total_revenue = sum(sale.grand_total() for sale in sales)
    total_sales   = sales.count()
    # calculate average sale
    average_sale  = total_revenue / total_sales if total_sales > 0 else 0

    return render(request, 'reports/sales_report.html', {
        'sales'       : sales,
        'total_revenue': total_revenue,
        'total_sales' : total_sales,
        'average_sale': average_sale,
    })


@role_required('accounts')
def scheme_report(request):
    # All scheme customers with their deposit totals
    customers = SchemeCustomer.objects.all()
    return render(request, 'reports/scheme_report.html', {'customers': customers})