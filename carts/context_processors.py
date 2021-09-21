from .models import Cart,CartItem
from .views import _cart_id
from django.http import HttpResponse
def counter(request):
    if 'admin'in request.path:
        return {}
    else:
     cart_count = 0
     try:
      cart = Cart.objects.filter(cart_id= _cart_id(request))
      cart_item = CartItem.objects.filter(cart=cart[:1])
      for cart_item in cart_item:
         cart_count += cart_item.quantity
     except Cart.DoesNotExist:
        cart_count = 0
     return dict(cart_count=cart_count)
