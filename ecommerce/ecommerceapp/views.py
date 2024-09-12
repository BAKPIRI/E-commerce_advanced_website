from math import ceil
from django.shortcuts import redirect, render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders
from django.contrib import messages
from ecommerceapp import keys
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError

import paypalrestsdk
import logging

from paypalrestsdk import Payment
import json
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    products= Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category','id')
    
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides= n // 4 + ceil((n / 4)-(n // 4))
        allProds.append([prod,range(1, nSlides), nSlides])
    params={'allProds':allProds}
    print(allProds)
    return render(request,"index.html",params )
def contact(request):
 if request.method=="POST":
    name=request.POST.get("name")
    email=request.POST.get("email")
    desc=request.POST.get("desc")
    pnumber=request.POST.get("pnumber")
    myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
    myquery.save()
    messages.info(request,"We will get back to you")
 return render(request,"contact.html" )
def about(request):
    return render(request,"about.html" )
def checkout(request):
   if not request.user.is_authenticated:
     messages.warning(request,"Login and Try Again")
     return redirect('/auth/login')
   if request.method=="POST": 
     items_json=request.POST.get('itemsjson','')
     name=request.POST.get('name','')
     amount=request.POST.get('amt','')
     email=request.POST.get('email','')
     adress1=request.POST.get('adress1','')
     adress2=request.POST.get('adress2','')
     city=request.POST.get('city','')
     state=request.POST.get('state','')
     zip_code=request.POST.get('zip_code','')
     phone=request.POST.get('phone','')
     Order = Orders(items_json=items_json,name=name,amount=amount,email=email,
     address1=adress1,address2=adress2,city=city,state=state,zip_code=zip_code,
     phone=phone)
     Order.save()
     update=OrderUpdate(order_id=Order.order_id,upate_desc="The order has been placed")
     update.save()
     thank=True
   #return render(request,'checkout.html')

    # PAYEMENT INTEGRATION
 
    
#    id=Order.order_id
#    oid=str(id)+"ShopyCart"


   
 #param_dict {
     
            
#            'ORDER_ID': 'oid',
#            'amount': amount,
#            'CUST_ID': 'sb-lmoj128808212@business.example.com',
#            'INDUSTRY_TYPE_ID': 'Retail',
#            'WEBSITE': 'WEBSTAGING',
#            'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL':'http://127.0.01:8000/handlerequest/',

# Placeholder for payment integration dictionaries  
     key_dic = {'public_key': keys.PK}   
     customer_dict = {
            'email': email,
            'lastname': name,
            'firstname': name,
        }
     context = {
    'customer': customer_dict,
    'key': key_dic,
    'amount': amount,
}   
     return render(request, 'paytm.html', context)
   return render(request,'checkout.html')
# @csrf_exempt=

# def handlerequest(request):
#    form=request.POST

#    response_dict={}
#    for i in form.keys():
#       response_dict[i]=form[i]
#       if i=='CHECKSUMHASH':
#          checksum=form[i]
#    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
#    if verify:
#       if response_dict['RESPCODE']=='01':
#         print('order succesful')
#         a=response_dict['ORDERID']
#         b=response_dict['TXNAMOUNT']
#         rid=a.replace("ShopyCart","")

#         print(rid)
#         filter2=Orders.objects.filter(order_id=rid)
#         print(filter2)
#         print(a,b)
#         for post1 in filter2:
#             post1.oid=a
#             post1.amountpaid=b
#             post1.paymentstatus="PAID"
#             post1.save()
#             print("run agede function")
#    else:
#       print('order was not succeful because'+ response_dict['RESPMSG'])
 
#    return render(request,'paymentstatus.html',{'response': response_dict})


# def profile(request):
#    if not request.user.is_authenticated:
#      messages.warning(request,"Login and Try Again")
#      return redirect('/auth/login')
#    currentuser=request.user.username
#    items=Orders.objects.filter(email=currentuser)
#    rid=""
#    for i in items:
#         print(i.oid)
#         myid=i.oid
#         rid=myid.replace("ShopyCart","")
    
#         print(rid)
#    status=OrderUpdate.objects.filter(order_id=int(rid))
   
#    context={"item":items}

#    for j in status:
#       print(j.upate_desc)
#       print(j.delivered)
#       print(j.timestamp)
#       context.update({"msg":j.upate_desc})
#       context.update({"dstatus":j.upate_desc})
#       context.update({"timestamp":j.upate_desc})
#    print(context)
#    return render(request,'profile.html',context)
def successful(request):
    return render(request,"successful.html" )
def cancelled(request):
    return render(request,"index.html" )







