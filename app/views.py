from app.webscrape import getProductUpdates
import json
from typing import Reversible
from django.conf.urls import url
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import refs_expression
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils import html
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Customer, Product, Cart, OrderPlaced, Ratings,Recommendation, Reward, Contact
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse
from .cosineSim import Similarity
import geopy
from geopy.geocoders import Nominatim
cat={"V":"Vegitables","F":"Fruits","LH":"Leafy and Herbs","SD":"Sale of the Day"}

class ProductView(View):
    def get(self, request):
        totalitem = 0
        rewardPoint=0
        recommended=[]  
        if request.user.is_authenticated:
            try:
                userInterests=Recommendation.objects.get(user=request.user)
                products=Product.objects.all()
                for product in products:
                    cosine=Similarity(userInterests.interests,product.title+" "+cat[product.category])
                    if cosine>0.30:  
                        recommended.append(product)
            except:
                recommended=""
        vegetables = Product.objects.filter(category='V')
        fruits = Product.objects.filter(category='F')
        leafyherbs= Product.objects.filter(category='LH')
       
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
           
        if len(recommended)<=0:recommended=False
        if request.user.is_authenticated:
            try:
                rewardObject=Reward.objects.get(user=request.user)
                rewardPoint+=rewardObject.rewardpoints
            except:
                rewardPoint=0

        return render(request, 'app/home.html',{'rewardpoints':rewardPoint,'recommended':recommended,'vegetables':vegetables, 'fruits':fruits, 'leafyherbs':leafyherbs, 'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem = len(Cart.objects.filter(user=request.user))    
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart, 'totalitem':totalitem}) 

class SearchView(TemplateView):
    template_name = 'app/search.html'

    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        #print(kw, "...................")
        results = Product.objects.filter(title__icontains=kw)
        #print(results)
        context["results"] = results

        return context
        




def vegetables(request):
    vegetables= Product.objects.filter(category='V')

    return render(request, 'app/vegetables.html',{'vegetables':vegetables})       

def fruits(request):
    fruits= Product.objects.filter(category='F')

    return render(request, 'app/fruits.html',{'fruits':fruits})     

def leafyherbs(request):
    leafyherbs= Product.objects.filter(category='LH')

    return render(request, 'app/leafy and herbs.html',{'leafyherbs':leafyherbs})   

def about(request):
   return render(request, 'app/about.html')     

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        content=request.POST.get('content')
        #print(name, email, phone, content)
        contact= Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
    return render(request, 'app/contact.html')    

    


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
        shipping_amount = 50.0
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
        c.quantity+=1
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


        



def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))   
        add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'totalitem':totalitem, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return redirect('/accounts/login/')





@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        lat=request.POST.get("latitude")
        print(type(lat))
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']  
            
            email = form.cleaned_data['email']   
            location = form.cleaned_data['location'] 
            mobile_number = form.cleaned_data['mobile_number']
            latitude = float(request.POST.get("latitude"))
            longitude =float( request.POST.get("longitude"))
            cordinates=latitude,longitude
            locator = Nominatim(user_agent="myGeocoder")
            location=locator.reverse(cordinates)
            response=location.raw 
            reg = Customer(user = usr, name=name,email=email, mobile_number=mobile_number,address=response["display_name"])
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
    rp=0
    user = request.user
    custid = request.GET.get('custid')
    paymentMethod = request.GET.get('paymentName')
    print(paymentMethod)
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        order=OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity,payment_method=paymentMethod)
        order.save()

        if order.total_cost<=100:
            rp=rp+1
        elif order.total_cost>100:
            rp=rp+2
        try:
            rewardPoint=Reward.objects.get(user=user)
            rPoint=rewardPoint.rewardpoints
            rewardPoint.rewardpoints=rPoint+rp
            rewardPoint.save()
        except:
            rewardPoint=Reward.objects.create(user=user,rewardpoints=rp)
            rewardPoint.save()
        try:
            recom=Recommendation.objects.get(user=user)
            recom.interests=recom.interests+" "+cat[c.product.category]+" "+c.product.title
            recom.save()
        except:
            recomm=Recommendation.objects.create(user=user,interests=cat[c.product.category]+" "+c.product.title)
            recomm.save()
        c.delete()
    return redirect('orders')    


@login_required
def addrating(request):
    if request.method=="POST":
         user=request.user
         rating =request.POST.get("rating")
         productId =request.POST.get("product")
         try:
            ratingModel=Ratings.objects.get(user=user)
            ratingModel.product=productId
            ratingModel.ratings=rating
            ratingModel.save()
         except:
            ratingModel=Ratings.objects.create(user=user,product=productId,ratings=rating)
            ratingModel.save()
         print(ratingModel)
        #  ratingModel.save()
         
    return JsonResponse({"ratings": "success"})


def maps(request):
		template = loader.get_template('app/maps.html')
		return HttpResponse(template.render({}, request))


def updateProducts(request):
    productUpdate=getProductUpdates() 
    products=Product.objects.all()
    for product in products:   
        for k,v in productUpdate.items(): 
            if any(x in k for x in product.title.split(" ")):
                
                pd=Product.objects.get(title=product.title) 
                pd.selling_price=int(v.split(" ")[1])-0.05*int(v.split(" ")[1])
                pd.save()

    return redirect("/")