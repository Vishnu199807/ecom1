from django import forms
from .models import *


class OrderUpdateForm(forms.Form):
    options=(
        ("dispatched","dispatched"),
        ("in-transit","in-transit")
    )
    status=forms.ChoiceField(choices=options,widget=forms.Select(attrs={"class":"form-select"}))
    expected_delivery_date=forms.DateField(widget=forms.DateInput(attrs={"class":"form-control","type":"date"}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('name', 'quantity', 'price', 'category', 'image', 'description')
