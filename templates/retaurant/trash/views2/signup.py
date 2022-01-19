from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import CustomerAddress, Customer
from django.views import View

from retaurant.models import Category



class Signup (View):
    def get(self, request):
        # categories = Category.objects.all()
        return render (request, 'signup.html')
        

    def post(self, request):
        postData = request.POST
     

        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None




        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             username=email,
                             phone_number=phone,
                             email=email,
                             password=password)


        error_message = self.validateCustomer (customer)

        # if not error_message:
        #     print (first_name, last_name, phone, email, password)
        #     customer.password = make_password (customer.password)
        #     customer.register ()
        #     return redirect ('homepage')
        # else:
        #     data = {
        #         'error': error_message,
        #         'values': value
        #     }
        #     return render (request, 'signup.html', data)


        #------------------------------
        

        # error_message_address = self.validateAddress (address)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()


            state = postData.get ('state')
            city = postData.get ('city')
            full_address = postData.get('full_address')

        

            value2 = {
                'state': state,
                'city': city,
                'full_address': full_address,
                
            }
            
            error_message_address = None

            address = CustomerAddress(
                state=state,
                city=city,
                full_address=full_address,
                customer=Customer.objects.get(email=customer.email)
                )
            error_message2 = self.validateAddress (address)
            if not error_message2 :
                address.save()
                return redirect ('homepage')
            else :
                customer.delete()
                data = {
                'error': error_message2,
                'values': value2
            }
            return render (request, 'signup.html', data)
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone_number:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone_number) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'

    def validateAddress(self, address):
        error_message = None
        if (not address.state):
            error_message = "Please Enter your State !!"
        elif len (address.state) < 3:
            error_message = 'First State must be 3 char long or more'
        elif not address.city:
            error_message = 'Please Enter your City'
        elif len (address.city) < 3:
            error_message = 'Last City must be 3 char long or more'
        elif not address.full_address:
            error_message = 'Enter your Full Address'
        # saving customer

        return error_message
