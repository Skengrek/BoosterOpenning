from django.contrib import admin
from cards.models import Card, Set, Booster


@admin.register(Card)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "rarity", "extension_id")


@admin.register(Set)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "series", "extension_id")


@admin.register(Booster)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("user", "get_set_id", "number")

    def get_set_id(self, obj):
        return obj.set.extension_id
    
    get_set_id.admin_order_field  = 'set'  #Allows column order sorting
    get_set_id.short_description = 'Extension ID'  #Renames column head
