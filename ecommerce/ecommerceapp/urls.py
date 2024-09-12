from django.urls import include, path
from ecommerceapp import views
urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('checkout/',views.checkout,name="checkout"),
    path('successful/',views.successful,name="successful"),
    path('cancelled/',views.cancelled,name="cancelled")
    
    
   # path('profile',views.profile,name="profile"),
    
]
