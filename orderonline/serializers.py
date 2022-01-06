from rest_framework import serializers
from accounts.models import Customer
from .models import Food,FoodCategory,MealCategory,RestaurantBranch

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email']
        

class FoodSerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = Food
        fields = "__all__"

class FoodCategorySerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = FoodCategory
        fields = "__all__"

class MealCategorySerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = MealCategory
        fields = "__all__"

class MealCategorySerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = MealCategory
        fields = "__all__"

class RestaurantBranchSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantBranch
        fields = "__all__"