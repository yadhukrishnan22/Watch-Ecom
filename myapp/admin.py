from django.contrib import admin

from myapp.models import Brand, IdealFor, Type, Product, ProductVarient, Color, OrderSummary

admin.site.register(Brand)

admin.site.register(IdealFor)

admin.site.register(Type)

admin.site.register(Product)

admin.site.register(ProductVarient)

admin.site.register(Color)

admin.site.register(OrderSummary)
