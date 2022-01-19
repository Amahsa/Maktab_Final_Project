from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def site_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_site_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def restaurant_manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_restaurant_manager,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_restaurant_manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_restaurant_manager or u.is_site_admin),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_site_admin or u.is_cutomer),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



from django.contrib.auth.decorators import login_required, user_passes_test

user_login_required = user_passes_test(lambda user: user.is_active, login_url='/login')
def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func




# class ProductExistsRequiredMixin:
    
#     def dispatch(self, request, *args, **kwargs):
#         if  Product.objects.filter(pk=1, activate=True):
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied



from django.shortcuts import redirect

class RedirectMixin:
    """
    Redirect to redirect_url if the test_func() method returns False.
    """

    redirect_url = '/login'

    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
        redirect_url = self.redirect_url
        # if not redirect_url:
        #     raise ImproperlyConfigured(
        #         '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
        #         '{0}.get_redirect_url().'.format(self.__class__.__name__)
        #     )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        test_result = self.get_test_func()()
        if not test_result:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class LoggedInRedirectMixin(RedirectMixin):
    def test_func(self):
        return self.request.user.is_authenticated

class ISAdminRedirectMixin(RedirectMixin):
    def test_func(self):
        return self.request.user.is_site_admin