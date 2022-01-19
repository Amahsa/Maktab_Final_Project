from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import Admin
from django.views import View



class SiteAdminSignupView (View):
    def get(self, request):
        print('SiteAdminSignupView GGGGGGGGGGG')
        return render (request, 'retaurant/site_dmin_signup.html')
        


    def post(self, request):
        print('SiteAdminSignupView PPPPPPPPPPPPPP')
        postData = request.POST

        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {}
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        admin =  Admin(first_name=first_name,
                             last_name=last_name,
                             username=email,
                             phone_number=phone,
                             email=email,
                             password=password)


        error_message = self.validateAdmin (admin)

        #------------------------------
        
        if not error_message:
            print('OKKKKKKKKKKKKKKKKKKK')
            print (first_name, last_name, phone, email, password)
            admin.password = make_password (admin.password)
            admin.save ()
                
            return redirect ('homepage')
        else:
            print('NOT OKKKKKKKKKKK')
            date = {}
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'retaurant/site_dmin_signup.html', data)

    def validateAdmin(self, admin):
        print(99999999999)
        error_message = None
        if (not admin.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (admin.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not admin.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (admin.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not admin.phone_number:
            error_message = 'Enter your Phone Number'
        elif len (admin.phone_number) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (admin.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (admin.email) < 5:
            error_message = 'Email must be 5 char long'
        elif Admin.objects.filter(email=admin.email):
            error_message = 'Email Address Already Registered..'
        return error_message

    



