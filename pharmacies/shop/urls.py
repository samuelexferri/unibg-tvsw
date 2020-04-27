from django.urls import path, include
from rest_framework import routers

from shop import views

app_name = 'shop'

router = routers.DefaultRouter()
router.register(r'pharmacy/api', views.PharmacyViewSet, basename='pharmacyapi')
router.register(r'category/api', views.CategoryViewSet, basename='categoryapi')
router.register(r'product/api', views.ProductViewSet, basename='productapi')
router.register(r'buyer/api', views.BuyerViewSet, basename='buyerapi')
router.register(r'review/api', views.ReviewViewSet, basename='reviewapi')
router.register(r'contact/api', views.ContactViewSet, basename='contactapi')

urlpatterns = [
    path('', views.homepage, name='home'),
    path(r'', include(router.urls)),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name="contact"),
    path('pharmacies/', views.pharmacy_list, name='pharmacies_list'),
    path('pharmacies/<id>/', views.pharmacy_detail, name='pharmacies_detail'),
    path('categories/<slug>/', views.categories, name='categories'),
    path('products/', views.product_list, name='products_list'),
    path('products/<id>', views.product_detail, name='products_detail'),
    path('search/', views.search, name='search'),
    path('sellproduct/', views.sell_product, name='sell_product'),
    path('buyitems/', views.buy_items, name='buy_items'),
    path('cart/', views.cart, name='cart'),
    path('resetcart/', views.reset_cart, name='reset_cart'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name="checkout"),
    path('<id>/addcart/', views.add_cart, name='add_cart'),
    path('<id>/addreview/', views.add_review, name='add_review'),
]
