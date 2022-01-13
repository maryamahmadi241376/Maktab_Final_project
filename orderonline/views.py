from django.http.response import JsonResponse
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from accounts.models import Address,CustomerAddress, RestaurantManager
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.db.models import Count,Max, Sum, fields
from .serializers import *
from .decorator import superuser_required, is_staff_required, customer_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# def search(request):
#     results=[]
#     if request.method == 'GET':
#         data = request.GET.get('search')
#         # if data == '':
#         #     data = 'None'
#         results = Menu.objects.filter(Q(food__food_name__icontains=data) | Q(branch__restaurant_branch_name__icontains=data))   
#     return render(request,"search/search.html",{'data':data,'results':results})

@superuser_required()
class FoodView(LoginRequiredMixin,TemplateView):
    template_name = "foods.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foods'] = Food.objects.all()
        return context


def show_foods(req):
    foods = Food.objects.all()
    menus = Menu.objects.all()
    most_seller_restaurant = RestaurantBranch.objects.filter(branch_menus__orderitems__order__customer_status = "order_confirmed").annotate(sum_totalprice=Sum("branch_menus__orderitems__order__total_price")).order_by("-sum_totalprice")[:10]

    most_seller_foods = Food.objects.all().filter(food_menu__orderitems__order__customer_status = "order_confirmed").annotate(sum_number=Sum("food_menu__orderitems__number")).order_by("-sum_number")[:10]

    return render(req, "home.html", {"foods": foods,"menus":menus,'most_seller_foods':most_seller_foods,'most_seller_restaurant':most_seller_restaurant})

class MostSellerRestaurant(TemplateView):
    template_name = "restaurant/branch_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_seller_restaurants'] = RestaurantBranch.objects.filter(branch_menus__orderitems__order__customer_status = "order_confirmed").annotate(sum_totalprice=Sum("branch_menus__orderitems__order__total_price")).order_by("-sum_totalprice")[:10]
        return context

@superuser_required()
class FoodCreate(CreateView):
    model = Food
    template_name = "websitemanager.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

@superuser_required()
class FoodUpdate(UpdateView):
    model = Food
    template_name = "update_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

@superuser_required()
class FoodDelete(DeleteView):
    model = Food
    template_name = "delete_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

@superuser_required()
class PostFoodCategoryCreate(CreateView):
    model = FoodCategory
    template_name = "food_category_form.html"
    success_url = reverse_lazy('add_food')
    fields = "__all__"   


def food(request,pk):  
    menus = Menu.objects.get(id = pk)
    food = Food.objects.get(food_menu__id = pk)
    if request.method == 'POST':
        #Get user account information
        try:
            customer = request.user.device
            if Customer.objects.get(username=request.user.device):
                c_customer = Customer.objects.get(username=request.user.device)
                c_customer.delete()
            
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(username=device,email=device+"@gmail.com",device=device)
        
        if Order.objects.filter(customer=customer).filter(customer_status="ordered") and Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer=customer):
            if (Menu.objects.filter(id = pk).values_list("branch__restaurant_branch_name").last())[0] == Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer=customer).values_list("branch__restaurant_branch_name").first()[0]:
                if ((Menu.objects.filter(id = pk).values_list('menu_number').last())[0]) >= int(request.POST['number']):  #موجودی انبار
                    order, created = Order.objects.get_or_create(customer=customer, customer_status='ordered')
                    orderItem, created = OrderItem.objects.get_or_create(order=order, menu=menus)
                    orderItem.number =request.POST['number']
                    orderItem.save()
                    return redirect('add_to_cart')
                else:
                    context = {'menus':menus, "food":food ,'msg':"not enough foods"}
                    return render(request, 'order_detail.html', context)

            else:
                return render(request, 'order_detail.html', {'menus':menus, "food":food ,'msg':"you should remove current orders."})
        else:

            if (Menu.objects.all().filter(id = pk).values_list('menu_number').last())[0]>= int(request.POST['number']):
                order, created = Order.objects.get_or_create(customer=customer, customer_status='ordered')
                orderItem, created = OrderItem.objects.get_or_create(order=order, menu=menus)
                orderItem.number =request.POST['number']
                orderItem.save()
                return redirect('add_to_cart')
            else:
                return render(request, 'order_detail.html', {'menus':menus, "food":food ,'msg':"not enough!"})
    return render(request, 'order_detail.html', {'menus':menus, "food":food })


def cart(request):
    if request.method =="POST":
        if request.user:
            orderitems = OrderItem.objects.filter(order__customer_status="ordered")
            total_price = sum([item.get_total for item in orderitems])
            device = request.COOKIES['device']
            branch_id = Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer__device=device).values_list("branch__id").first()[0]
            branch_order = Order.objects.get(customer_status = "ordered")
            branch_address = request.POST['cart_address']
            customer_address = CustomerAddress.objects.get(id=branch_address)
            branch = RestaurantBranch.objects.get(id = branch_id)


            branch_order.branch = branch

            branch_order.total_price = total_price
            branch_order.customer_status = "order_confirmed"
            branch_order.address = customer_address
            branch_order.save()
            return render(request,"cart.html",{'msg':"no orderitems available!"})
        else:
            return reverse('add_to_cart')

    try:
        customer = request.user.device
        if Customer.objects.get(username=request.user.device):
            c_customer = Customer.objects.get(username=request.user.device)
            c_customer.delete()


    except:
        device = request.COOKIES['device']
        customer = device
    customer_address = CustomerAddress.objects.all()
    orderitems=OrderItem.objects.filter(Q(order__customer__device=customer) & Q(order__customer_status="ordered"))
    food = Food.objects.filter(food_menu__orderitems__order__customer__device=customer)
    orders = Order.objects.filter(customer__device=customer).filter(customer_status = "ordered")

    return render(request, 'cart.html', {'orders':orders,"orderitems": orderitems,"food":food,"customer_address":customer_address})

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = "delete_food.html"
    success_url = reverse_lazy("add_to_cart")
    fields = "__all__"

#restaurant panel

@is_staff_required()
class RestaurantBranchUpdate(UpdateView):
    model = RestaurantBranch
    template_name = "restaurant/branch_address_edit.html"
    success_url = reverse_lazy('restaurant_panel')
    fields= "__all__"

@is_staff_required()
class MenuCreate(CreateView):
    model = Menu
    template_name = "restaurant/create_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = ["food","menu_number","price"]

    def post(self, request, *args, **kwargs):
        branch = RestaurantBranch.objects.get(manager__username = self.request.user.username)
        food = request.POST["food"]
        foods = Food.objects.get(id = food)
        price = request.POST["price"]
        menu_number = request.POST["menu_number"]
        form = self.get_form()
        if form.is_valid():
            new = Menu.objects.create(branch = branch,food = foods , price = price ,menu_number = menu_number )
            return redirect("restaurant_panel")
        else:
            return self.form_invalid(form)


@is_staff_required()
class ManagerMenus(TemplateView):
  template_name = "restaurant/branch.html"
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    context["manager_menus"] = Menu.objects.filter(branch__manager__username = self.request.user.username)
    context["branchs"] = RestaurantBranch.objects.get(manager__username=self.request.user.username)
    context["manager"] = RestaurantManager.objects.get(username=self.request.user.username)
    context["orders"] = Order.objects.filter(branch__manager__username=self.request.user.username).exclude(customer_status = "ordered")
    return context

@is_staff_required()
class MenuUpdate(UpdateView):
    model = Menu
    template_name = "restaurant/edit_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = ["menu_number","price"]

@is_staff_required()
class MenuDelete(DeleteView):
    model = Menu
    template_name = "restaurant/delete_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"

class BranchList(ListView):
    # contecxt_object_name = "branchs"
    model = RestaurantBranch
    template_name = "restaurant/restaurant.html"

class BranchDetail(DetailView):
    model = RestaurantBranch
    queryset = RestaurantBranch.objects.all()
    template_name = "restaurant/branch_detail.html"


class CustomerOrders(LoginRequiredMixin,TemplateView):
    template_name = "customer/customer_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.filter(customer_address__customer_id__username=self.request.user.username)
        context['orders'] = Order.objects.filter(customer__username=self.request.user.username)
        return context
        
def search_result(req):
    if req.is_ajax():
        res = None
        result = req.POST.get('data')
        q = Menu.objects.filter(Q(food__food_name__icontains=result) | Q(branch__restaurant_branch_name__icontains=result))
        if len(q) > 0 and len(result) > 0:
            data =[]
            for i in q:
                item ={
                    'pk' : i.pk,
                    'food':{'food_name':i.food.food_name, 'img':i.food.food_image.url},
                    'menu': {'branch_name':i.branch.restaurant_branch_name, 'category':i.branch.food_category.food_category_name},
                    'price': i.price,
                    'menu_number': i.menu_number
                }
                data.append(item)
            res = data
        else:
            res = "No Food Or Restaurant Found..."

        return JsonResponse({'dataa':res})
    return JsonResponse({})



def get_info_search(req, pk):
    obj = get_object_or_404(Menu, pk=pk)
    return render(req, 'search/search.html', {'obj':obj})