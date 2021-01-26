from django.contrib import admin

import bakery.models as models

admin.site.register(models.User)
admin.site.register(models.BakeryIngredient)
admin.site.register(models.BakeryItemIngredient)
admin.site.register(models.Order)
