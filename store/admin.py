from django.contrib import admin

# Register your models here.

from store.models import Category,Size,Brand,AgeBetween,Material,Colour,Product

admin.site.register(Size)

admin.site.register(Category)

admin.site.register(Brand)

admin.site.register(AgeBetween)

admin.site.register(Material)


admin.site.register(Colour)

admin.site.register(Product)