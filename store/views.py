from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from .models import Product
def store(request,category_slug=None):
     categories = None
     products = None
    # paged_product = None
     if category_slug != None :
         categories = get_object_or_404(Category,slug=category_slug)
         print("------------")
         print(categories)
         products = Product.objects.filter(category=categories,is_available=True)
         paginator = Paginator(products, 1) # Show 3 products per page.
         page_number = request.GET.get('page')
         paged_product = paginator.get_page(page_number)
         print("------------")
         print(products.query)
         products_count = products.count()
     else:
         products =  Product.objects.all().filter(is_available=True).order_by('id')
         paginator = Paginator(products, 3) # Show 3 products per page.
         page_number = request.GET.get('page')
         paged_product = paginator.get_page(page_number)
         products_count = products.count()
     context = {
               "products":paged_product,
               "products_count":products_count
     }
     return render(request, 'store/store.html',context)


def product_detail(request,category_slug=None,product_slug=None):

     try:
       single_product = Product.objects.get(category__slug=category_slug,slug =product_slug,is_available=True)
       in_cart_item = CartItem.objects.filter(cart__cart_id =_cart_id(request),product=single_product).exists()

       #return HttpResponse(in_cart_item)
       #exit()

     except Exception as e:
        raise e

     context = {
               "single_product":single_product,
              "in_cart_item" : in_cart_item,
               }
     return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

            products_count = products.count()
    context = {'products':products,
    'products_count':products_count,
    }
    return render(request, 'store/store.html',context)
