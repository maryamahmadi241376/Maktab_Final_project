from accounts.models import Address
from orderonline.forms import FoodForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from datetime import timezone
from datetime import datetime
from django.db.models import Count,Max, Sum
from .serializers import *
from .decorator import superuser_required, is_staff_required, customer_required
from django.db.models import Q

# def foodView(req):
#     foods = Food.objects.all()
#     form = FoodForm
#     return render(req, "websitemanager.html", {"form": form})

def foodView(req):
    foods = Food.objects.all()
    return render(req, "foods.html", {"foods": foods})

def show_foods(req):
    foods = Food.objects.all()
    menus = Menu.objects.all()
    most_seller_restaurant = RestaurantBranch.objects.filter(branch_menus__orderitems__order__customer_status = "order_confirmed").annotate(sum_totalprice=Sum("branch_menus__orderitems__order__total_price")).order_by("-sum_totalprice")[:10]

    most_seller_foods = Food.objects.all().filter(food_menu__orderitems__order__customer_status = "order_confirmed").annotate(sum_number=Sum("food_menu__orderitems__number")).order_by("-sum_number")[:10]

    return render(req, "home.html", {"foods": foods,"menus":menus,'most_seller_foods':most_seller_foods,'most_seller_restaurant':most_seller_restaurant})

# # @api_view(['POST','GET'])
# # def addfood(request):
# #     print("aaaaaaaaaaaaaaaaa")
# #     foods = FoodForm(request.POST)
# #     print(request.POST)
    
# #     print(foods.errors)
    
# #     if foods.is_valid():
        
# #         foods.save()
# #         api_root = reverse_lazy('foods', request=request)
# #     return Response(foods.data)


class FoodCreate(CreateView):
    model = Food
    template_name = "websitemanager.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class FoodUpdate(UpdateView):
    model = Food
    template_name = "update_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class FoodDelete(DeleteView):
    model = Food
    template_name = "delete_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class PostFoodCategoryCreate(CreateView):
    model = FoodCategory
    template_name = "food_category_form.html"
    success_url = reverse_lazy('add_food')
    fields = "__all__"   


# def cart(request,pk):
	
#     food = get_object_or_404(Food,pk=pk)
#     orderitem, created = OrderItem.objects.get_or_create(food=food)
#     order_qs = Order.objects.filter(customer=request.user, customer_status=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         #check order item
#         if order.order_item.filter(food__id=food.id).exists():
#             orderitem.number += 1
#             orderitem.save()
#         else:
#             order.order_item.add(orderitem)
#     else:
#         order = Order.objects.create(customer=request.user,delivery_time=timezone.now(),order_date=datetime.now())
#         order.items.add(orderitem)
#     return reverse_lazy('home')


def food(request,pk):  
    menus = Menu.objects.get(id = pk)
    food = Food.objects.get(food_menu__id = pk)
    if request.method == 'POST':
        #Get user account information
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device,username=device)

        menu = (Menu.objects.all().filter(id = pk).values_list('menu_number').last())[0]
        if menu >= int(request.POST['number']):  #موجودی انبار
            order, created = Order.objects.get_or_create(customer=customer, customer_status='ordered',total_price=1000)
            orderItem, created = OrderItem.objects.get_or_create(order=order, menu=menus,number=request.POST['number'])
            orderItem.number =request.POST['number']
            orderItem.save()
            return redirect('add_to_cart')
        else:
            context = {'menus':menus, "food":food ,'msg':"not enough foods"}
            return render(request, 'order_detail.html', context)

    context = {'menus':menus, "food":food }
    return render(request, 'order_detail.html', context)


def cart(request):
    # if request.method =="POST":
    #     if request.user:
    #         orderitems = OrderItem.objects.all().filter(order__customer__email=request.user)
    #         total_price = sum([item.get_total for item in orderitems])

    #         branch_orderitem = RestaurantBranch.objects.filter(branch_menus__orderitems__order__customer__email= request.user)
    #         branch_address = CustomerAddress.objects.filter(customer_id=request.user.id)

    #         branch_order = Order.objects.get(customer_status = "ordered")

    #         branch_order.branch = branch_orderitem
    #         branch_order.total_price = total_price
    #         branch_order.customer_status = "order_confirmed"
    #         branch_order.address = branch_address
    #         branch_order.save()

    try:
        customer = request.user.customer
        customer_address = Address.objects.filter(customer__username = customer.username)

        device = request.COOKIES['device']
        orderitems=OrderItem.objects.filter(order__customer__username=customer.username)
        food = Food.objects.filter(food_menu__orderitems__order__customer__username=customer.username)
        orders = Order.objects.filter(customer__username=customer.username)

    except:
        device = request.COOKIES['device']
        orderitems=OrderItem.objects.filter(order__customer__username=device)
        food = Food.objects.filter(food_menu__orderitems__order__customer__username=device)
        orders = Order.objects.filter(customer__username=device) 
        customer, created = Customer.objects.get_or_create(device=device ,username = device)
        

    context = {'orders':orders,"orderitems": orderitems,"food":food}
    return render(request, 'cart.html', context)


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = "delete_food.html"
    success_url = reverse_lazy("home")
    fields = "__all__"

# class AddressView(CreateView):
#     model = Address
#     template_name = "choose_address.html"
#     success_url = reverse_lazy('cart')
#     fields= "__all__"

# # def most_selling_foods(req):
   
#     # foods_deliverd=( Food.objects.all().filter(food__foodmenu__order_id__status = "Peyment"))
#     # my_dict ={}
#     # for i in foods_deliverd:
#     #     name = i.name
#     #     order_item_of_one_food= OrderItem.objects.all().filter(food_menu_id__food_id__name = name).aggregate(Count("number"))["number__count"]
#     #     # print(order_item_of_one_food)
#     #     my_dict.update({i:order_item_of_one_food})
#     # best_foods = dict(sorted(my_dict.items(), key=lambda item: item[1]))




