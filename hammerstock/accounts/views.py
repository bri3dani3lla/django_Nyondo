from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# LANDING PAGE
def landing(request):
# If the user is already logged in, send them straight to stock dashboard
    if request.user.is_authenticated:
        return redirect('stock_dashboard')
# Otherwise show the landing page
    return render(request, 'accounts/landing.html')


# LOGIN

def login_view(request):
# If already logged in, no need to see login page
    if request.user.is_authenticated:
        return redirect('stock_dashboard')

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
            return redirect('stock_dashboard')
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


