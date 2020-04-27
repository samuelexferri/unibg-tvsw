from django import forms

from shop.models import Product, Buyer, Contact, Review


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


class SellProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pharmacy', 'name', 'image', 'category', 'description', 'brand', 'quantity', 'price', 'shipping_fee']


class BuyerDeliveryForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['full_name', 'phone', 'city', 'address']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']
