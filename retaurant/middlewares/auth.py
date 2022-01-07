from typing import Annotated
from django.shortcuts import redirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print(111,request.session.get('customer'))
        print(2222)
        returnUrl = request.META['PATH_INFO']
        print(333,request.META['PATH_INFO'])
        print(request.user)
        if not request.user.is_authenticated:
            return redirect(f'accounts/login?return_url={returnUrl}')
        elif not request.user.is_customer :
            return redirect(f'accounts/login?return_url={returnUrl}')
        else :

        # if not request.session.get('customer'):
        #    return redirect(f'accounts/login?return_url={returnUrl}')


            response = get_response(request)
            return response

    return middleware