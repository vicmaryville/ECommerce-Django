from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from Store.models import Product, Profile
import datetime

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})


def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

          

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session info
        my_shipping = request.session.get('my_shipping')

        # gather order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create a  shipping address from session info

        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals



        if request.user.is_authenticated:
            # logged in
            user = request.user

            # Create an order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # get thr order id
            order_id = create_order.pk
            
           # Get product info
            for product in cart_products:
                 # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get product quantity
               
                for key,value in quantities.items():
                    if int(key) == product_id:
                       create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, price=price, quantity=value)
                       create_order_item.save()


            messages.error(request, "Order Processed Successfully")
            return redirect('home')
        else:
            # not logged in
            create_order = Order( full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk
            
           # Get product info
            for product in cart_products:
                 # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get product quantity
               
                for key,value in quantities.items():
                    if int(key) == product_id:
                       create_order_item = OrderItem(order_id=order_id, product_id=product_id, price=price, quantity=value)
                       create_order_item.save()
            # Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]

            # Delete cart from database
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete cart from database
            current_user.update(old_cart="")

            messages.success(request, "Order Processed Successfully")
            return redirect('home')
        
    else:
        messages.error(request, "Acess Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
			# Get The Billing Form
            billing_form = PaymentForm()
            shipping_form = request.POST
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            # Not logged in
			# Get The Billing Form
            billing_form = PaymentForm()
            shipping_form = request.POST
            return render(request, "payment/billing_info.html", { "cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
    else:
        messages.error(request, "You must be logged in to checkout.")
        return redirect('login')




def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    # Initialize shipping_form outside the conditional blocks
    shipping_form = None

    if request.user.is_authenticated:
        try:
            # Try to get existing shipping address for logged-in user
            shipping_user = ShippingAddress.objects.get(user=request.user)
            shipping_form = ShippingForm(instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            # If no existing shipping address, create a new form
            shipping_form = ShippingForm()
    else:
        # For guest checkout, create a new shipping form
        shipping_form = ShippingForm()

    # Consolidate rendering to a single return statement
    return render(request, 'payment/checkout.html', {
        "cart_products": cart_products, 
        "quantities": quantities, 
        "totals": totals, 
        "shipping_form": shipping_form
    })
 




def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
