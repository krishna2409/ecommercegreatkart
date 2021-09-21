from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Variation
from .models import Cart, CartItem

# Create your views here.
def cart(request,quantity = 0,total=0,cart_items=None):
    try:
       tax= 0
       grand_total = 0
       cart_item_count = 0
       cart = Cart.objects.get(cart_id = _cart_id(request))
       cart_items = CartItem.objects.filter(cart=cart,is_active=True)

       for cart_i in cart_items:
          total += (cart_i.product.price * cart_i.quantity)
          quantity += cart_i.quantity
       tax = (2*total)/100
       grand_total = tax + total


    except ObjectDoesNotExist:
        pass #just ignore
    context = {"cart_items":cart_items,"total_price":total,"quantity":quantity,"grand_total":grand_total,"tax":tax}
    return render(request, 'store/cart.html',context)
def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method=='POST':
        for item in request.POST:
            key = item
            value=request.POST[key]
            #print(key,value)

            try:
                variation = Variation.objects.get(product = product,variation_category__iexact = key, variation_value__iexact = value)
                print(variation)
                product_variation.append(variation)
                print("check variation here2: ")
            except:
                pass

    #return HttpResponse(product)
    #exit()
    #creating cart
    try:
       cart = Cart.objects.get(cart_id=_cart_id(request))
    except  Cart.DoesNotExist:
       cart = Cart.objects.create(cart_id=_cart_id(request))
       cart.save()
    #creating cartItems
    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        id = []
        ex_var_list = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            print(ex_var_list)

        if product_variation in ex_var_list:
           #return HttpResponse('true')
           index =ex_var_list.index(product_variation)
           item_id = id[index]
           item = CartItem.objects.get(product=product,id=item_id)
           item.quantity +=1
           item.save()
        else:
           #return HttpResponse('false')
           item = CartItem.objects.create(product = product,quantity=1,cart=cart)
           if len(product_variation) > 0:
             item.variations.clear()
             item.variations.add(*product_variation)
           item.save()
    else:
             cart_item = CartItem.objects.create( product=product,cart=cart,quantity=1)
             if len(product_variation) > 0:
                 cart_item.variations.clear()
                 cart_item.variations.add(*product_variation)
             cart_item.save()
    return redirect('cart')
    #return render(request,'store/cart.html',context)

#dcrement cartitem
def dec_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product =get_object_or_404(Product,id=product_id)
    try:
        cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#remove cartItem
def remove_cartitem(request,product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_items = CartItem.objects.filter(cart=cart,product=product, id=cart_item_id)
    cart_items.delete()
    return redirect('cart')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
