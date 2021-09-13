from django.shortcuts import render,get_object_or_404
from category.models import Category

# Create your views here.
from .models import Product
def store(request,category_slug=None):
     categories = None
     products = None
     if category_slug != None :
         categories = get_object_or_404(Category,slug=category_slug)
         print("------------")
         print(categories)
         products = Product.objects.filter(category=categories,is_available=True)
         print("------------")
         print(products.query)
         products_count = products.count()
     else:
         products =  Product.objects.all().filter(is_available=True)
         products_count = products.count()
     context = {
               "products":products,
               "products_count":products_count
     }
     return render(request, 'store/store.html',context)


def product_detail(request,category_slug=None,product_slug=None):

     try:
       single_product = Product.objects.get(category__slug=category_slug,slug =product_slug,is_available=True)
     except Exception as e:
        raise e

     context = {
               "single_product":single_product,
               }
     return render(request,'store/product_detail.html',context)