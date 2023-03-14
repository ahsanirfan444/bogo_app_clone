from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def vendor_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, dashboard_url = "home"):
    """ Decorator to check views is the login user is vendor role, if not then redirect to login """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_vendor(),
        login_url=dashboard_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    
    return actual_decorator


def admin_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, dashboard_url = "home"):
    """ Decorator to check views is the login user is admin role, if not then redirect to login """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin(),
        login_url=dashboard_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    
    return actual_decorator


def guest_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, dashboard_url = "home"):
    """ Decorator to check views is the user is anonymous role, if not then redirect to same page """

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=dashboard_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    
    return actual_decorator