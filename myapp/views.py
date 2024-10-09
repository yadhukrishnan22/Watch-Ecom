from django.shortcuts import render, redirect

from myapp.forms import RegistrationForm, LoginForm, UserProfileForm, ReviewForm, DeliveryForm

from django.views.generic import View, UpdateView, TemplateView

from django.contrib.auth import authenticate, login, logout

from myapp.models import UserProfile, Product, ProductVarient, Color, CartItems, OrderSummary, Brand, IdealFor,Reviews, Type

from django.urls import reverse, reverse_lazy

from myapp.decorators import signin_required

import razorpay

from decouple import config

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.contrib import messages

KEY_SECRET = config('KEY_SECRET')

KEY_ID = config('KEY_ID')


class SignUpView(View):

    def get(self, request, *args, **kwargs):

        form_instance = RegistrationForm()

        return render(request, 'store/register.html', {'form':form_instance})
    
    
    def post(self, request, *args, **kwargs):

        form_instance = RegistrationForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success("Successfully registered")

            return redirect('sign-in')
        
        messages.error("Failed to register")

        
        return render(request, 'store/register.html', {'form':form_instance})


class SignInView(View):

    def get(self, request, *args, **kwargs):

        form_instance = LoginForm()

        print(form_instance)

        return render(request, 'store/login.html', {'form':form_instance})
    
    def post(self, request, *args, **kwargs):

        form_instance = LoginForm(request.POST)

        if form_instance.is_valid():

            data = form_instance.cleaned_data

            user_obj = authenticate(request, **data)

            if user_obj:

                login(request, user_obj)

                messages.success(request, "Login Successfull")

                return redirect('index')
            
            messages.error(request, "Login Failed")
            
            return render(request, 'store/login.html', {'form':form_instance})


@method_decorator(signin_required, name='dispatch')
class SignOutView(View):

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect('publicindex')


@method_decorator(signin_required, name='dispatch')
class UserProfileUpdateView(UpdateView):

    model = UserProfile

    form_class = UserProfileForm

    template_name = 'store/profile_edit.html'


    def get_success_url(self):

        return reverse('index')


@method_decorator(signin_required, name='dispatch')
class IndexView(View):

    def get(self, request, *args, **kwargs):

        brand = Brand.objects.values('name')

        idealfor = IdealFor.objects.all()

        type = Type.objects.all()

        qs = Product.objects.all()

        return render(request, 'store/index2.html', {'brands':brand, 'products':qs, 'gender':idealfor, 'types':type})
    

    def post(self, request, *args, **kwargs):

        brand = request.POST.get("brandbox")
        
        brand_values = Brand.objects.values('name')

        idealfor = IdealFor.objects.all()

        type = Type.objects.all()

        gender_value = request.POST.get('genderBox')

        type_value = request.POST.get('typeBox') 


        if brand:

            brand_obj = Brand.objects.get(name = brand)

            brand_obj = brand_obj.id

            if gender_value:

                qs = Product.objects.filter(brand_obj = brand_obj, for_obj = gender_value)
            
            elif type_value:

                qs = Product.objects.filter(brand_obj = brand_obj, type_obj = type_value)
            
            elif gender_value and type_value:

                qs = Product.objects.filter(brand_obj = brand_obj, for_obj = gender_value, type_obj = type_value)           
                    
            else:

                qs = Product.objects.filter(brand_obj = brand_obj)
            

            return render(request, 'store/index2.html', {'brands':brand_values, 'products':qs,'gender':idealfor, 'types':type})
                     
        if gender_value:

            if type_value:

                qs = Product.objects.filter(for_obj = gender_value, type_obj = type_value)
            
            else:

                qs = Product.objects.filter(for_obj = gender_value)

            return render(request, 'store/index2.html', {'brands':brand_values,'products': qs, 'gender':idealfor, 'types':type})
        
        if type_value:

            qs = Product.objects.filter(type_obj = type_value)          

        return render(request, 'store/index2.html', {'brands':brand_values, 'products':qs, 'gender':idealfor, 'types':type})

                
@method_decorator(signin_required, name='dispatch')
class ProductDetailsView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        details = Product.objects.get(id = id)

        review_comments = Reviews.objects.filter(product_object = id)

        qs = ProductVarient.objects.filter(product_obj = id)

        return render(request, 'store/product_details.html', {'varients':qs,'details':details, 'reviews':review_comments})


@method_decorator(signin_required, name='dispatch')
class ProductVarientView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        qs = ProductVarient.objects.get(id = id)

        color = ProductVarient.objects.filter(id = id).values('color_obj__color_name')
        
        color_name = {}

        for c in color:

            a = c['color_obj__color_name']

        return render(request, 'store/product_varient.html', {'varients':qs, 'color':a})


@method_decorator(signin_required, name='dispatch')
class AddToCart(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        product_varient_obj = ProductVarient.objects.get(id = id)


        CartItems.objects.create(cart_object = request.user.basket,
                                 product_varient_object = product_varient_obj)
        
        print('successfully added to cart')

        return redirect('index')


@method_decorator(signin_required, name='dispatch')
class CartListView(View):

    def get(self, request, *args, **kwargs):

        qs = request.user.basket.basket_items.filter(is_order_placed = False)

        total = request.user.basket.cartlist_total

        print(total)

        return render(request, 'store/cart.html', {'cartitems':qs})


@method_decorator(signin_required, name='dispatch')
class CartItemsDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        CartItems.objects.get(id = id).delete()

        print('Item deleted from cart')

        return redirect('cart-list')


@method_decorator(signin_required, name='dispatch')
class DeliveryDetailsView(View):

    def get(self, request, *args, **kwargs):

        form_instance = DeliveryForm()

        return render(request, 'store/delivery_details.html', {'form':form_instance})
    
    def post(self, request, *args, **kwargs):

     

        amount = request.user.basket.cartlist_total * 100

        cart_items = request.user.basket.basket_items.filter(is_order_placed = False)

        form_instance = DeliveryForm(request.POST)

        
        if form_instance.is_valid():

            data = form_instance.cleaned_data

            order_summary_obj = OrderSummary.objects.create(
            user_object = request.user,
            total = request.user.basket.cartlist_total,
            **data
        
        )
        
            
        for ci in cart_items:

            order_summary_obj.product_varient_object.add(ci.product_varient_object)

            order_summary_obj.save()

        if order_summary_obj.payment_method == 'Cash':


            for ci in cart_items:

                ci.is_order_placed = True

                ci.save() 
                
            return redirect('index')
        
        

        return redirect('payment')


@method_decorator(signin_required, name='dispatch')
class CheckOutView(View):

    def get(self, request, *args, **kwargs):

        cart_items = request.user.basket.basket_items.filter(is_order_placed = False)

        client = razorpay.Client(auth= (KEY_ID, KEY_SECRET))

        amount = request.user.basket.cartlist_total * 100

        data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        OrderSummary.objects.filter(user_object = request.user, payment_method = 'Upi', order_id__isnull = True).update(order_id = payment.get('id'))

        for ci in cart_items:

            ci.is_order_placed = True

            ci.save() 
        
        context = {

            "key": KEY_ID,
            "amount": data.get("amount"),
            "currency": data.get("currency"),
            "order_id": payment.get("id")
        }
        
     
        return render(request, "store/payment.html", context)



# @method_decorator(signin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerificationView(View):

    def post(self, request, *args, **kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        order_summary_object = OrderSummary.objects.get(order_id = request.POST.get("razorpay_order_id"))

        # login(request, order_summary_object.user_object)

        try:

            client.utility.verify_payment_signature(request.POST)

            print('payment successfull')

            order_id = request.POST.get('razorpay_order_id')

            OrderSummary.objects.filter(order_id = order_id).update(is_paid = True)

        except:

            print("not Successfull")      

        
        return redirect('index')


@method_decorator(signin_required, name='dispatch')
class MyPurchaseView(View):

    model = OrderSummary

    context_object_name = 'orders'

    def get(self, request, *args, **kwargs):

        qs = OrderSummary.objects.filter(user_object = request.user, is_paid = True).order_by('-created_date')
        

        return render(request, 'store/ordersummary.html', {'orders':qs})


class MyPendingPaymentsView(View):

    def get(self, request, *args, **kwargs):

        qs = OrderSummary.objects.filter(user_object = request.user, order_id__isnull = True, payment_method = 'Cash').order_by('-created_date')

        return render(request, 'store/pending_payments.html', {'orders':qs})


class PublicIndexView(View):

    def get(self, request, *args, **kwargs):

        brand = Brand.objects.values('name')

        idealfor = IdealFor.objects.all()

        type = Type.objects.all()

        qs = Product.objects.all()
        

        return render(request, 'store/public_index.html', {'brands':brand, 'products':qs, 'gender':idealfor, 'types':type})
    

    def post(self, request, *args, **kwargs):

        brand = request.POST.get("brandbox")

        idealfor = IdealFor.objects.all()

        type = Type.objects.all()

        brand_values = Brand.objects.values('name')

        gender_value = request.POST.get('genderBox')

        type_value = request.POST.get('typeBox')     
        
        if brand:

            brand_obj = Brand.objects.get(name = brand)

            brand_obj = brand_obj.id

            if gender_value:

                qs = Product.objects.filter(brand_obj = brand_obj, for_obj = gender_value)
            
            elif type_value:

                qs = Product.objects.filter(brand_obj = brand_obj, type_obj = type_value)
            
            elif gender_value and type_value:

                qs = Product.objects.filter(brand_obj = brand_obj, for_obj = gender_value, type_obj = type_value)           
                    
            else:

                qs = Product.objects.filter(brand_obj = brand_obj)
            

            return render(request, 'store/public_index.html', {'brands':brand_values, 'products':qs})
        
        
        
        if gender_value:

            if type_value:

                qs = Product.objects.filter(for_obj = gender_value, type_obj = type_value)
            
            else:

                qs = Product.objects.filter(for_obj = gender_value)

            return render(request, 'store/public_index.html', {'products': qs})
        
        if type_value:

            qs = Product.objects.filter(type_obj = type_value)

          

        return render(request, 'store/public_index.html', {'brands':brand_values, 'products':qs, 'gender':idealfor, 'types':type})


class PublicProductDetailsView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        details = Product.objects.get(id = id)

        review_comments = Reviews.objects.filter(product_object = id)

        qs = ProductVarient.objects.filter(product_obj = id)

        return render(request, 'store/public_product_details.html', {'varients':qs,'details':details, 'reviews':review_comments})


class PublicProductVarientView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        qs = ProductVarient.objects.get(id = id)

        color = ProductVarient.objects.filter(id = id).values('color_obj__color_name')
        
        color_name = {}

        for c in color:

            a = c['color_obj__color_name']

        return render(request, 'store/public_product_varient.html', {'varients':qs, 'color':a})
    

class TestView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'store/test.html')


class ReviewCreateView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        form_instance = ReviewForm()

        qs = ProductVarient.objects.get(id = id)


        return render(request, 'store/reviews.html', {'form':form_instance, 'product':qs})
    

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        product_varient_obj = ProductVarient.objects.get(id = id)

        form_instance = ReviewForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object = request.user

            form_instance.instance.product_object = product_varient_obj.product_obj

            form_instance.save()

            return redirect('index')
        
        return render(request, 'store/review.html', {'form':form_instance})





 



    



    







