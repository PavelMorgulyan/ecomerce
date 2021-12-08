from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, customerOrders
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .decorators import unaunthenticated_user, allowed_users

# @allowed_users
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

# @unaunthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request,username=username, password=password)

		try:
			if user is not None:
				login(request, user)
				return redirect('store')
			else:
				messages.info(request, 'Username OR password in not correct')
				
		except:
			print("Cant redirect to store")
			pass
	context = {}
	return render(request, 'store/login.html', context)

def logoutPage(request):
	logout(request)
	print("User logouted")
	return redirect('login')

@login_required(login_url='login') # Стандартный декоратор из django.contrib.auth.decorators
def userPage(request):
	orders = customerOrders(request)['orders']
	help = orders[:]
	orders_q_set = orders[:len(help) - 1]
	orders_q_set.append(help[len(help):])
	orders_q_set.remove([])
	orderitems = customerOrders(request)['orderitems']
	shipping_addresses = customerOrders(request)['shipping_address']
	customer_name = request.user.customer.name
	customer_vk_link = request.user.customer.vk_link
	customer_phone = request.user.customer.phone
	customer_email = request.user.customer.email
	context = {'orders':orders_q_set, 'orderitems':orderitems, 'shipping_addresses':shipping_addresses,
	 'customer_name': customer_name, 'customer_vk_link':customer_vk_link, 'customer_phone':customer_phone, 'customer_email':customer_email}
	return render(request, 'store/user.html', context)

@unaunthenticated_user
def registrationPage(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('store')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username=form.cleaned_data.get('username')
				group = Group.objects.get(name='customer') # Добавили пользователя user в группу customer
				user.groups.add(group)

				email=form.cleaned_data.get('email')

				Customer.objects.create(
					user=user,
					name=username,
					email=email,
					#phone="",
					#vk_link="",
					)

				messages.success(request, 'Новый пользователь был создан под именем ' + username)
				return redirect('login') # переходим в login.html

		context = {'form':form}
		return render(request, 'store/registration.html', context)

# @login_required(login_url='login')
def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)

	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def newUserInfo(request):
	data = json.loads(request.body)
	Customer.objects.all().filter(user_id=data['form']['id']).update(
			name=data['form']['name'],
			email=data['form']['email'],
			vk_link = data['form']['vklink'],
			phone = data['form']['phone'])
	User.objects.all().filter(id=data['form']['id']).update(
			username=data['form']['name'],
			email=data['form']['email'],
			)
	return JsonResponse('New info submitted..', safe=False)