from .models import FoodCategory, Food , MealCategory
from django import forms

class FoodForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print(self.fields.values())
        for name in self.fields.keys():
            
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Food
        exclude = ['food_created_date']

class FoodCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodCategoryForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = FoodCategory
        fields = ("__all__")

class MealCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MealCategoryForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = MealCategory
        fields = ("__all__")