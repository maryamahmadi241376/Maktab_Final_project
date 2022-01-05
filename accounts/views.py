from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from accounts.forms import ManagerSignUpForm,CostumerSignUpForm
from orderonline.models import RestaurantBranch
from .models import *
from django.urls import reverse_lazy


# @login_required
def managers_signup(request):
    return render(request, "account/signup.html")

# class AdminCreate(CreateView):
#     model = Admin
#     template_name = "account/signup.html"
#     success_url = reverse_lazy('home')
#     fields = ['email','password']

class ManagerCreate(CreateView):
    model = ManagerSignUpForm
    template_name =  "account/signup.html"
    success_url = reverse_lazy('home')
    fields = ['email','password']

class CustomerCreate(CreateView):
    model = CostumerSignUpForm
    template_name = "account/customer_signup.html"
    success_url = reverse_lazy('home')
    fields = ['email','password','address']

class AddressCreate(CreateView):
    model = Address
    template_name = "account/address.html"
    success_url = reverse_lazy('add_customer')
    fields = "__all__"

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})