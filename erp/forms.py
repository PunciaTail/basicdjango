from django import forms
from .models import Product, Inbound, Outbound
# form


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'description', 'price', 'size', 'image']


class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['name', 'quantity']


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['name', 'quantity']
