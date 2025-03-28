from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager  # Import the custom manager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    contact=models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Link the custom user manager
    objects = CustomUserManager()

    # Set the unique identifier to be the email field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # You can add extra required fields here

    def __str__(self):
        return self.email
    

    #-----------------------------------------------------------------
class Category(models.Model):
    name=models.CharField(max_length=100)
    choice=('Active','Active'),('Disable','Disable'),
    status=models.CharField(max_length=100,choices=choice)
    img=models.ImageField(upload_to='Category',default='',blank=True)

    def __str__(self):
        return self.name


#---------------------------------------------------Structure for Brand-------------------------------------------

class Brand(models.Model):
    name=models.CharField(max_length=150)
    img=models.ImageField(upload_to='Brands',default='',blank=True)
    choice=('Active','Active'),('Disable','Disable')
    status=models.CharField(max_length=100,choices=choice)

    def __str__(self):
        return self.name
    
#----------------------------------------------------Structure for Product----------------------------------------

class Product(models.Model):
    title=models.CharField(max_length=100, null=True)
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete= models.CASCADE , null=True)
    mrp=models.CharField(max_length=255)
    discount=models.IntegerField()
    code=models.CharField(max_length=100)
    images=models.ImageField(upload_to='Products',default="", blank=True)
    description=models.TextField()
    brand=models.ForeignKey(Brand, on_delete= models.CASCADE, null=True)
    choice=("Active","Active"),("Disable","Disable")
    status=models.CharField(max_length=100,choices=choice, null=True)
    stock=models.CharField(max_length=100)
    trendingchoice=(('Y','Yes'),('N','No'))
    trendingstatus=models.CharField(max_length=255,choices=trendingchoice, default='')

    
    def __str__(self):
        return self.name
    


class Cart(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    cart_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name



class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.IntegerField()
    order_id=models.CharField(max_length=255)
    order_date=models.DateField(auto_now_add=True)
    choice=(('Success','Success'),
            ('Pending','Pending'),
            ('Delivered','Delivered'),
            ('Cancelled','Cancelled'),
            ('Refund','Refund'),
            ('Return','Return'),)
    status=models.CharField(max_length=255,choices=choice)


    def __str__(self):
        return self.order_id

class Billing(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField()
    contact=models.CharField(max_length=255)
    address=models.TextField()
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    pincode=models.IntegerField()
    country=models.CharField(max_length=255)
    amount=models.CharField(max_length=255)
    choice=(('Online','Online'),('COD','COD'))
    payment_mode=models.CharField(max_length=255,choices=choice)
    billing_date=models.DateField(auto_now_add=True)  


    def __str__(self):
        return self.first_name  