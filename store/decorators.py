from django.http import HttpResponse
from django.shortcuts import redirect


def unaunthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('store')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.group.exists():
				group = request.user.group.all()[0].name

			if group in allowed_roles:
				print('Working:', allowed_users)
				return view_func(request, *args, **kwargs)
			
		return wrapper_func
	return decorator
