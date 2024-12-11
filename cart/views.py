from django.shortcuts import render, get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    try:
    # Get the cart
        cart = Cart(request)
    # Test for POST
    #if request.POST.get('action') == 'post':
        # Get the product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty', 1))
        # Look up the product
        product = get_object_or_404(Product, id=product_id)
        print(f"Attempting to add product {product_id}, qty: {product_qty}")

        # Save to session
        cart.add(product=product, qty=product_qty)

        # get the cart quantiyu
        cart_quantity = cart.__len__()

        print(f"Cart quantity after add: {cart_quantity}")

        return JsonResponse({
            'qty': cart_quantity, 
            'success': True,
            'message': 'Product added to cart'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=400)
        

       

        # for obj in my_queryset:
        #     print(obj)

        # Get the quantity
        cart_quantity = cart.__len__()

        # Return response
        return JsonResponse({
            'qty': cart_quantity, 
            'success': True,
            'message': 'Product added to cart'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=400)

        

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get the product
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        #return redirect('cart_summary')

        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'product': product_id , 'qty': cart_quantity})
        messages.success(request, ("Item Deleted From Shopping Cart..."))

        return response

    

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get the product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})

		#return redirect('cart_summary')
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response