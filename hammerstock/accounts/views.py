from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stock.models import Product, StockEntry, Supplier
from sales.models import Sale
from scheme.models import SchemeCustomer, Deposit 
from accounts.models import Profile


# Create your views here.
# LANDING PAGE
def landing(request):
# If the user is already logged in, send them straight to stock dashboard
    if request.user.is_authenticated:
        return redirect_by_role(request.user) 
# Otherwise show the landing page
    return render(request, 'accounts/landing.html')

def redirect_by_role(user):
    """
    Check the user's role and redirect them to the 
    correct dashboard for their role. 
    """
    try:
        role = user.profile.role
        if role == 'manager':
            return redirect('stock_dashboard')
        elif role == 'attendant':
            return redirect('sales_dashboard')
        elif role == 'accounts':
            return redirect('reports_dashboard')
        else:
            return redirect('stock_dashboard')
    except:
        #if user has no profile yet send to stock dashboard 
        return redirect('stock_dashboard')


# LOGIN

def login_view(request):
# If already logged in, no need to see login page
    if request.user.is_authenticated:
        return redirect_by_role('stock_dashboard')

    error = None  # we will use this to show error messages in the template

    if request.method == 'POST':
        # Get the username and password from the submitted form
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username and password are correct
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Correct credentials — log the user in
            login(request, user)
            # redirect based on role after login
            return redirect_by_role(user)
        else:
            # Wrong credentials — show an error
            error = 'Invalid username or password. Please try again.'

    return render(request, 'accounts/login.html', {'error': error})


# LOGOUT

# @login_required means only logged in users can access this view
@login_required
def logout_view(request):
    # Log the user out and send them to the landing page
    logout(request)
    return redirect('landing')

def access_denied(request):
    """ 
    Show this page when a user tries to access a page they
    are not allowed to see.
    """
    return render(request, 'accounts/access_denied.html') 


# ADMIN DASHBOARD

@login_required
def admin_dashboard(request):
    # only superuser can access this
    if not request.user.is_superuser:
        return redirect('/access-denied/')

    # system overview
    total_users    = User.objects.count()
    total_products = Product.objects.count()
    total_sales    = Sale.objects.count()
    all_sales      = Sale.objects.all()
    total_revenue  = sum(sale.grand_total() for sale in all_sales)
    total_suppliers = Supplier.objects.count()
    total_scheme   = SchemeCustomer.objects.count()

    # all users with their roles
    users = User.objects.all().order_by('username')

    # recent activity
    recent_stock  = StockEntry.objects.all().order_by('-created_at')[:5]
    recent_sales  = Sale.objects.all().order_by('-created_at')[:5]
    recent_deposits = Deposit.objects.all().order_by('-deposit_date')[:5]

    return render(request, 'accounts/admin_dashboard.html', {
        'total_users'    : total_users,
        'total_products' : total_products,
        'total_sales'    : total_sales,
        'total_revenue'  : total_revenue,
        'total_suppliers': total_suppliers,
        'total_scheme'   : total_scheme,
        'users'          : users,
        'recent_stock'   : recent_stock,
        'recent_sales'   : recent_sales,
        'recent_deposits': recent_deposits,
    }) 
def redirect_by_role(user):
    if user.is_superuser:
        return redirect('admin_dashboard')
    try:
        role = user.profile.role
        if role == 'manager':
            return redirect('stock_dashboard')
        elif role == 'attendant':
            return redirect('sales_dashboard')
        elif role == 'accounts':
            return redirect('reports_dashboard')
        else:
            return redirect('stock_dashboard')
    except:
        return redirect('stock_dashboard') 
    
    from django.contrib.auth.models import User
from accounts.models import Profile


@login_required
def register_user(request):
    # only superuser can register new users
    if not request.user.is_superuser:
        return redirect('/access-denied/')

    error = None
    success = None

    if request.method == 'POST':
        username   = request.POST['username']
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        password1  = request.POST['password1']
        password2  = request.POST['password2']
        role       = request.POST['role']

        # validation
        if password1 != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = f'Username "{username}" already exists.'
        else:
            # create the user
            user = User.objects.create_user(
                username   = username,
                first_name = first_name,
                last_name  = last_name,
                password   = password1,
            )
            # create their profile with role
            Profile.objects.create(user=user, role=role)
            success = f'User "{username}" registered successfully!'

    return render(request, 'accounts/register_user.html', {
        'error'  : error,
        'success': success,
    })


@login_required
def edit_user(request, pk):
    if not request.user.is_superuser:
        return redirect('/access-denied/')

    user = get_object_or_404(User, pk=pk)

    error   = None
    success = None

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name  = request.POST['last_name']
        role            = request.POST['role']

        # update role
        profile      = user.profile
        profile.role = role
        profile.save()
        user.save()
        success = f'User "{user.username}" updated successfully!'

    return render(request, 'accounts/edit_user.html', {
        'u'      : user,
        'error'  : error,
        'success': success,
    })