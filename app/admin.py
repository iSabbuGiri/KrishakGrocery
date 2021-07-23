from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced, 
    Ratings,Recommendation,Reward, Contact
)
admin.site.register(Ratings)
admin.site.register(Recommendation)
admin.site.register(Reward)
admin.site.register(Contact)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name', 'email', 'mobile_number', 'address']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price', 'category' ,'product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','customer_info', 'product', 'product_info', 'quantity', 'ordered_date', 'status', 'payment_method']

   
    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}" >{}</a>', link, obj.customer.name) 

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}" >{}</a>', link, obj.product.title) 
    