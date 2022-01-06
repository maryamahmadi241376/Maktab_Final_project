from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .forms import ManagerSignUpForm,CostumerSignUpForm
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q



# @login_required
# def managers_signup(request):
#     return render(request, "account/signup.html")

# class AdminCreate(CreateView):
#     model = Admin
#     template_name = "account/signup.html"
#     success_url = reverse_lazy('home')
#     fields = ['email','password']

class ManagerCreate(CreateView):
    form_class = ManagerSignUpForm
    template_name =  "account/signup.html"
    success_url = reverse_lazy('home')

class CustomerCreate(CreateView):
    form_class = CostumerSignUpForm
    template_name = "account/customer_signup.html"
    success_url = reverse_lazy('home')

class AddressCreate(CreateView):
    model = Address
    template_name = "account/address.html"
    success_url = reverse_lazy('add_customer')
    fields = "__all__"

def address_create(request):
	if request.method == "POST":
		state = request.POST['state']
		city = request.POST['city']
		street = request.POST['street']
		pluque = request.POST['pluque']
		is_main_address = request.POST["it_is"]

		device = request.COOKIES['device']
		customer = request.user
		customer , create = Customer.objects.get_or_create(email = customer)
		address  = Address.objects.create(state=state,city = city,street = street,pluque=int(pluque))
		if is_main_address == "True":
			q1 = Q(is_main_address =True)
			print(q1)
			q2 = Q(customer_id__email = customer)
			print(q2)
			print(customer)
			
			edit = CustomerAddress.objects.get(q1 & q2)
			edit.is_main_address = False
			edit.save()
			
			
			customeraddress = CustomerAddress.objects.create(customer_id = customer , address_id = address,is_main_address=True)
			return redirect('cart')
	return render(request,'choose_address.html')


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {email}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"login_form":form})