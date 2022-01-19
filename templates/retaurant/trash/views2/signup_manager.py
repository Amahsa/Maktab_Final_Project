from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import Manager,Address
from ..models import Category, Restaurant,Branch
from django.views import View



class ManagerSignup (View):
    def get(self, request):
        categories = Category.objects.all()
        return render (request, 'manager_signup.html' ,{'category_list' : categories })
        
    def post(self, request):
        print('ooooooooooooooooooo')

        postData = request.POST  

        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')

        restaurant_name = postData.get ('restaurant_name')
        branch_name = 'main branch'

        state = postData.get ('state')
        city = postData.get ('city')
        full_address = postData.get('full_address')

        category = postData.get('category')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'state': state,
            'city': city,
            'full_address': full_address,
            'restaurant_name':restaurant_name
        }

        error_message = None


        manager = Manager (first_name=first_name,
                             last_name=last_name,
                             username=email,
                             phone_number=phone,
                             email=email,
                             password=password)

        restaurant = Restaurant(name=restaurant_name)         

        address = Address(
                state=state,
                city=city,
                full_address=full_address,
                # customer=manager.objects.get(email=manager.email)
                )     

        error_message = self.validateManager (manager,address)
        # error_message2 = self.validateAddress ()

        
        if not error_message :
            print (first_name, last_name, phone, email, password)
            manager.password = make_password (manager.password)


            manager.save()
            print(12,'manager.save')
            address = Address.objects.create(
                state=state,
                city=city,
                full_address=full_address,
                )
            restaurant.save()
            print(12,'restaurant.save')
            branch = Branch.objects.create(
                name = branch_name,
                address=address,
                manager=Manager.objects.get(email=manager.email),
                restaurant=restaurant,
                category=Category.objects.get(name=category),
                )
            print(33333,'restaurant.save')
            return redirect ('homepage')
                
        else :
                # customer.delete()
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)
        # else:
        #     data = {
        #         'error': error_message,
        #         'values': value
        #     }
        #     return render (request, 'signup.html', data)

    def validateManager(self, manager , address):
        error_message = None
        if (not manager.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (manager.first_name) < 3:
            manager = 'First Name must be 3 char long or more'
        elif not manager.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (manager.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not manager.phone_number:
            error_message = 'Enter your Phone Number'
        elif len (manager.phone_number) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (manager.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (manager.email) < 5:
            error_message = 'Email must be 5 char long'
        # elif manager.isExists ():
        #     error_message = 'Email Address Already Registered..'
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
        elif not address.full_address:
            error_message = 'Enter your Full Address'
        # saving manager

        return error_message
