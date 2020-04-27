from django.contrib import admin

from shop.models import Review, Category, Product, Buyer, Contact, Pharmacy

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)

admin.site.register(Contact)

admin.site.register(Pharmacy)


class BuyerAdmin(admin.ModelAdmin):
    readonly_fields = ['product']


admin.site.register(Buyer, BuyerAdmin)
