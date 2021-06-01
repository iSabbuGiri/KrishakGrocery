from django.shortcuts import render, redirect
from .models import Customer, Product, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitem = 0
        vegetables = Product.objects.filter(category='V')
        fruits = Product.objects.filter(category='F')
        leafyherbs= Product.objects.filter(category='LH')
        saleofday = Product.objects.filter(category='SD')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
           
        return render(request, 'app/home.html',{'vegetables':vegetables, 'fruits':fruits, 'leafyherbs':leafyherbs,'saleofday':saleofday, 'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem = len(Cart.objects.filter(user=request.user))    
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart, 'totalitem':totalitem}) 

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product = product).save()
    return redirect('/cart')


def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        
        totalitem = len(Cart.objects.filter(user=request.user))   
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 30.0
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount': totalamount, 'amount': amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')    



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))     
        c.quantity += 1
        c.save()    
        amount = 0.0
        shipping_amount = 30.0
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        #print(cart_product)


        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
           

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount' : amount + shipping_amount
        }   
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user== request.user]


        
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
           


        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }    

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user== request.user]


        
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
           


        data = {
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }    

        return JsonResponse(data)


        

def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))   
        add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'totalitem':totalitem, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')



def mobile(request):
 return render(request, 'app/mobile.html')



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})        

def checkout(request):
 return render(request, 'app/checkout.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']  
            
            email = form.cleaned_data['email']   
            location = form.cleaned_data['location'] 
            mobile_number = form.cleaned_data['mobile_number']
            reg = Customer(user = usr, name=name,email=email, location=location, mobile_number=mobile_number)
            reg.save()
            messages.success(request, 'Profile have been saved successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})       

    
@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        #print(cart_product)
    if cart_product:

        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount  
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))      
    
    return render(request, 'app/checkout.html', {'totalamount': totalamount, 'cart_items': cart_items, 'add':add, 'totalitem':totalitem})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')    

