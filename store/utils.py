import json
from .models import *

def cookieCart(request):

	# Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)
	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		# We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']
			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'image':product.image}, 'quantity':cart[i]['quantity'],
				'digital':product.digital,'get_total':total,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		print("customer:", customer)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		print("User is not authenticated")
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def customerOrders(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		orders = Order.objects.all().filter(customer_id=customer.id)
		orderitems = []
		shipping_address = []
		for order_id in orders:
			temp_orderitems = OrderItem.objects.all().filter(order_id=order_id)
			temp_shipping_address = ShippingAddress.objects.all().filter(order_id=order_id)
			shipping_address.append(temp_shipping_address)
			orderitems.append(temp_orderitems)
		orderitems = dict(zip([i for i in range(len(orderitems)-1)], orderitems[:-1]))
		shipping_address = dict(zip([i for i in range(len(shipping_address)-1)], shipping_address[:-1]))
	return {'orders':orders, 'orderitems':orderitems, 'shipping_address':shipping_address}

class ListAsQuerySet(list):
	def __init__(self, *args, model, **kwargs):
		self.model = model
		super().__init__(*args, **kwargs)
	
	def filter(self, *args, **kwargs):
		return self # we can custom filter
	
	def order_by(self, *args, model, **kwargs):
		return self

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order