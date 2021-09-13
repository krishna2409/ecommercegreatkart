from django.shortcuts import render
from store.models import Product
def home(request):
     products = Product.objects.all().filter(is_available=True)
     print("************************************************************")
     print(products)
     print(products.query)
     print(type(products))
     #print(type(name, bases, dict))
     context = {'products' : products}
     return render(request, 'home.html',context)
