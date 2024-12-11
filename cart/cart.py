from Store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session if it exists
        cart = self.session.get('session_key')

        # if the user is new, no seession key exists
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Ensure cart is a dictionary
        if not isinstance(cart, dict):
            cart = {}

        # Making sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, qty):
        product_id = str(product)
        product_qty = str(qty)
        print(f"Adding product: {product_id}, Quantity: {product_qty}")
        print(f"Current cart before add: {self.cart}")

    # Logic to add product to cart
        if product_id in self.cart:
            print(f"Product {product_id} already in cart")
        else:
            self.cart[product_id] = int(product_qty)
            print(f"Added product {product_id} with quantity {product_qty}")
            
        self.session.modified = True
        print(f"Cart after modification: {self.cart}")



        # Deal wiith logged in user
        if self.request.user.is_authenticated:
            # # Get the user
            # user_id = self.request.user.id
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3': 1, '4': 1} to {'3': '1', '4': '1'}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))
            print(f"Cart after modification: {self.cart}")

    def add(self, product, qty=1):
        product_id = str(product.id)
        product_qty = str(qty)
        print(f"Adding product: {product_id}, Quantity: {product_qty}")
        print(f"Current cart before add: {self.cart}")

    # Logic to add product to cart
        if product_id in self.cart:
            print(f"Product {product_id} already in cart")
        else:
            self.cart[product_id] = int(product_qty)
            print(f"Added product {product_id} with quantity {product_qty}")
            
        self.session.modified = True
        print(f"Cart after modification: {self.cart}")



        # Deal wiith logged in user
        if self.request.user.is_authenticated:
            # # Get the user
            # user_id = self.request.user.id
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3': 1, '4': 1} to {'3': '1', '4': '1'}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))

    # def add(self, product, quantity):
    #     # Get the product id
    #     product_id = str(product.id)
    #     product_qty = str(quantity)

    #     # Making sure cart is available on all pages of site
    #     if product_id not in self.cart:
    #         pass
    #     else:
    #         self.cart[product_id] = product_qty

    #     self.session.modified = True
        
    # def cart_total(self):
    #          # Get Product IDS
    #          product_ids = self.cart.keys()
    #     # lookup those keys in product db
    #     products = Product.objects.filter(id__in=product_ids)
    #     # loop through products and add to cart
    #     quantities = self.cart

    #     total = 0
    #     for key, value in quantities.items():
    #         key = int(key)
    #         for product in products:
    #             if product.id == key:
    #                 if product.is_sale:
    #                     total = total + (product.sale_price * value)
    #                 else:
    #                     total = total + (product.price * value)

        
    #     return total

    def cart_total(self):
        # Get Product IDS
        product_ids = self.cart.keys()
        # lookup those keys in product db
        products = Product.objects.filter(id__in=product_ids)
        # loop through products and add to cart
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        
        return total
       

    def __len__(self):
        return sum(self.cart.values())
    
    def  get_products(self):
        # Get the ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products
        products = Product.objects.filter(id__in=product_ids)

        # return products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get the cart
        self.cart[product_id] = int(product_qty)
        self.session.modified = True
        # Deal wiith logged in user

        if self.request.user.is_authenticated:
            # # Get the user
            # user_id = self.request.user.id
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3': 1, '4': 1} to {'3': '1', '4': '1'}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))

        x = self.cart
        return x
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

         # Deal wiith logged in user
        if self.request.user.is_authenticated:
            # # Get the user
            # user_id = self.request.user.id
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3': 1, '4': 1} to {'3': '1', '4': '1'}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))

        x = self.cart
        return x