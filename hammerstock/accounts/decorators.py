from django.shortcuts import redirect 


def role_required(*roles):
    """ 
    Use this decorator on any view to restrict access to specific roles only.
    example:
    @role_required('manager')
    def stock_dashboard(request):
    
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # check if user is logged in
            if not request.user.is_authenticated:
                return redirect('/login/')
            # superuser can access everything
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            # check if user has a profile and role
            try:
                role = request.user.profile.role
                if role in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('/access-denied/')
            # except:
            #     return redirect('/access-denied/') 
            except Exception as e:
                print(f"DECORATOR ERROR: {e}")
                return redirect('/access-denied/')
        return wrapper
    return decorator  
