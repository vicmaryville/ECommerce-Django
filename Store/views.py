from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart



def search(request):
    # determine if they fill out the form
    if request.method == "POST":
        searched = request.POST['searched']

        # query the proucts DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
                    # test for null
        if not searched:
            messages.success(request, "No Product Found.... please try again")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})


def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

  


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # fill the form?
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            # is the form valid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated successfully!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'update_password.html', {'form': form})
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to update your password.")
        return redirect('home')


def update_user(request):
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST or None, instance=current_user)

            if user_form.is_valid():
                user_form.save()
                
                login(request, current_user)
                messages.success(request, "Your account has been updated!")
                return redirect('home')
            
            return render(request, 'update_user.html', {'user_form': user_form})
        
        else:
            messages.error(request, "You must be logged in to update your profile.")
            return redirect('home')



       



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        context = {
            'products': products,
            'category': category,
        }
        return render(request, 'category.html', context)
    except Category.DoesNotExist:
        messages.error(request, f"Category '{foo}' does not exist")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product, 'ts':"take"}) 


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products}) 


def about(request):
    return render(request, 'about.html', {})

def  login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)


            # do some shoppin cart...
            current_user = Profile.objects.get(user__id=request.user.id)

            # Get thier saved cart from db
            saved_cart = current_user.old_cart
            # convert database string to python dictionary
            if saved_cart:
                 #convert to dictionary using JSON
                 converted_cart = json.loads(saved_cart)
                 #  Add  the loades cart dictionary to our session
                 # get the cart
                 cart = Cart(request)
                 # loop through the cart
                 for key, value in converted_cart.items():
                    cart.db_add(product=key, qty=value)


            messages.success(request, "You have been logged in!..")
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.....Thanks for shopping with us")
    return redirect('home')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm  # Ensure this import is correct

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in user
            user = authenticate(username=username, password=password)
            if user is not None:  # Check if user is authenticated
                login(request, user)
                messages.success(request, "Username created successfully. Please fill out your info below!....")
                return redirect('update_info')
           
        else:
            messages.error(request, "Whoops! Something went wrong. Please try again.")
            return redirect('signup')
    else:
        return render(request, 'signup.html', {'form': form})