from django.contrib import admin
from store.models import *
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','user','rate','product',)


class CartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','total']
    list_filter = ['user']
 




admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart, CartAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ShippingAddress)