
from app.emailNotification import sendEmailNotification
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import fields
from django.db.models.deletion import CASCADE



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    mobile_number = models.CharField(max_length=200)
    address=models.CharField(max_length=225,default="ktm")
    
  
   

    def __str__(self) :
        return str(self.id)




CATEGORY_CHOICES = (
    ('V','Vegetables'),
    ('F', 'Fruits'),
    ('LH', 'Leafy and Herbs'),
   

)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self) :
        return str(self.id)
        
    def save(self, *args, **kwargs):
        sendEmailNotification({
            "title":self.title,"sp":self.selling_price
        })
        super().save(*args, **kwargs)  # Call the "real" save() method.
        

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return str(self.id)  


    @property  
    def total_cost(self):
        return self.quantity * self.product.selling_price        

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

METHOD = (
    ("Cash on Delivery", "Cash on Delivery"),
    ("Paypal", "Paypal"),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    
    @property  
    def total_cost(self):
        return self.quantity * self.product.selling_price        


class Ratings(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=CASCADE)
    product=models.IntegerField(null=False)
    ratings=models.IntegerField(null=False,default=0)

class Recommendation(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=CASCADE)
    interests=models.CharField(max_length=255)

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rewardpoints=models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.user.username+"rewardpoints"

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self) :
        return 'Message from ' + self.name