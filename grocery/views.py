from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import random as r
import razorpay
#login custom user

def loginuser(request):
    category=Category.objects.filter(status='Active')
    product=Product.objects.filter(status='Active')
    latest=Product.objects.filter(status='Active')
    trending=Product.objects.filter(status='Active',trendingstatus='Y')
    if request.method == 'POST':
        email=request.POST.get('email')
        password = request.POST.get('pwd1')
        u = authenticate(email=email, password=password)
        if u is not None:
            login(request, u)
            return redirect('mainpage')
        else:
            msg = "Invalid Username & Password"
            return render(request, 'login.html', {'msg':msg})
    return render(request, 'index.html',{'category':category,'product':product,'latest':latest,'trending':trending})

# signup custom user

def signupuser(request):
    if request.method=='POST' :
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        contact=request.POST.get('contact')
        pwd1=request.POST.get('pwd1')
        pwd2=request.POST.get('pwd2')
        if pwd1==pwd2:
            user=CustomUser.objects.create_user(email=email, first_name=first_name,last_name=last_name,password=pwd1,contact=contact)
        
            user.save()
        return redirect('loginuser')
      
    return render(request,'signup.html')

#-----------------------------Home Page--------------
def home(request):
    if request.user.is_authenticated:
        category=Category.objects.filter(status='Active')
        product=Product.objects.filter(status='Active')
        latest=Product.objects.filter(status='Active')
        trending=Product.objects.filter(status='Active',trendingstatus='Y')[0:5]
        counter=Cart.objects.filter(user=request.user).values().count()
        cart=Cart.objects.filter(user=request.user)
        total=0
        for c in cart:
            total+=int(c.product.mrp)*int(c.qty)
        return render(request, 'index.html', {'category':category,'product':product,'latest':latest,'trending':trending,'counter':counter,'total':total})
    else:
        category=Category.objects.filter(status='Active')
        product=Product.objects.filter(status='Active')
        latest=Product.objects.filter(status='Active')
        trending=Product.objects.filter(status='Active',trendingstatus='Y')
        counter=0
        total=0

        return render(request, 'index.html', {'category':category,'product':product,'latest':latest,'trending':trending,'counter':counter,'total':total})


def category(request,id):
    category=Category.objects.filter(status='Active')
    product=Product.objects.filter(category=id)
    latest=Product.objects.filter(status='Active')
    counter=Cart.objects.filter(user=request.user).values().count()
    cart=Cart.objects.filter(user=request.user)
    total=0
    for c in cart:
        total+=int(c.product.mrp)*int(c.qty)

    return render(request,'categories.html',{'category':category,'product':product,'latest':latest,'counter':counter,'total':total})


def showproductdetails(request,id):
    categories=Category.objects.filter(status='Active')
    product=Product.objects.get(id=id)
    category=product.category
    allcategory=Category.objects.filter(product=id)
    related=Product.objects.filter(status='Active',category=category)
    counter=Cart.objects.filter(user=request.user).values().count()
    cart=Cart.objects.filter(user=request.user)
    total=0
    for c in cart:
        total+=int(c.product.mrp)*int(c.qty)

    return render(request,'productdetails.html',{'allcategory':allcategory,'product':product,'related':related,'counter':counter,'categories':categories,'total':total})

def addtocart(request):
    if request.user.is_authenticated:
        user=request.user
        product=request.GET.get('product')
        pid=Product.objects.get(id=product)
        qty=request.GET.get('qty')
        cart,created=Cart.objects.get_or_create(product=pid,user=user)
        if not created:
            cart.qty += int(qty)
            print(cart.qty)
        else:
            cart.qty=qty
        cart.save()
        return HttpResponse('Added to Cart')
    else:
        return HttpResponse('Login')


@login_required
def showcart(request):
    if request.user.is_authenticated:
        category=Category.objects.filter(status='Active')
        cart=Cart.objects.filter(user=request.user)
        counter=Cart.objects.filter(user=request.user).values().count()
        total=0
        for c in cart:
            total+=int(c.product.mrp)*int(c.qty)
        if total>=1000:
            sc=0
        else:
            sc=100
        netamount=total+sc
        return render(request,'cart.html',{'category':category,'cart':cart, 'counter':counter, 'total':total,'shippingcharge':sc,'net':netamount})
           
    else:
        cart=[]
        counter=0
        category=Category.objects.filter(status='Active')
        return render(request,'cart.html',{'category':category,'cart':cart, 'counter':counter})
    
def deletecart(request):
    id=request.GET.get('id')
    cart=Cart.objects.get(id=id)
    cart.delete()
    return HttpResponse('Item Deleted')

def updatecart(request):
    id=request.GET.get('id')
    nqty=request.GET.get('qty')
    cart=Cart.objects.get(id=id)
    cart.qty=nqty
    cart.save()
    return HttpResponse(' Updated ')


    
def checkout(request):
    cart=Cart.objects.filter(user=request.user)
    counter=Cart.objects.filter(user=request.user).values().count()
    uid=request.user
    order_id='ORD'+str(r.randint(1000,9999))
    total=0
    for c in cart:
        total+=int(c.product.mrp)*int(c.qty)
    if total>=1000:
        sc=0
    else:
        sc=100

    netamount=total+sc

    if request.POST.get('placeorder'):
        for x in cart:
            order=Order.objects.create(user=uid, product=x.product ,qty=x.qty ,order_id=order_id ,status='Success')
            order.save()
            product=Product.objects.get(id=x.product.id)
            product.stock=int(product.stock)-int(x.qty)
            product.save()


        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        street=request.POST.get('street')
        landmark=request.POST.get('landmark')
        address=street +","+ landmark
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        pincode=request.POST.get('pincode')
        amount=request.POST.get('amount')
        payment_mode=request.POST.get('payment')
        # order= request.POST.get('orderid')
        order=Order.objects.filter(order_id=order_id).first()

        bill=Billing.objects.create(user=request.user, first_name=first_name, last_name=last_name,email=email, contact=contact, address=address ,city=city, state=state, country=country, pincode=pincode, amount=amount, payment_mode=payment_mode, order_id=order)
        bill.save()
        cart.delete()
        if payment_mode=='Online':
            return render(request,'payment.html',{'amount': int(request.POST.get('amount'))*100})
        else:
            pass
        
    return render(request,'checkout.html',{'cart':cart,'total':total,'counter':counter,'orderid':order_id,'shippingcharge':sc,'net':netamount})

@csrf_exempt
def complete_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        return render(request,"complete_payment.html", {'amount': amount*100 })
    
def myorders(request):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.filter(user=user)
        counter=Cart.objects.filter(user=request.user).values().count()
        cart=Cart.objects.filter(user=request.user)
        total=0
        for c in cart:
            total+=int(c.product.mrp)*int(c.qty)

        return render(request,'myorders.html',{'order':order,'total':total,'counter':counter})

 


def logoutuser(request):
    logout(request)
    return redirect('loginuser')
