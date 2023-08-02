from django.contrib import admin
from cards.models import Card, Booster, UsersBooster


admin.site.register(Card)
admin.site.register(Booster)
admin.site.register(UsersBooster)
