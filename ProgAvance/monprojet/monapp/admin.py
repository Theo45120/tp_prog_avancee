from django.contrib import admin
from .models import Product, ProductItem, ProductAttribute, ProductAttributeValue, Commande

class ProductFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin) :
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'online':
            return queryset.filter(status=1)
        if self.value() == 'offline':
            return queryset.filter(status=0)

class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    filter_vertical = ("attributes",)
    raw_id_fields = ["attributes"]

def set_product_online(modeladmin, request, queryset):
    queryset.update(status=1)
set_product_online.short_description = "Mettre en ligne"

def set_product_offline(modeladmin, request, queryset):
    queryset.update(status=0)
set_product_offline.short_description = "Mettre hors ligne"

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductItemAdmin,]
    list_display = ["id", "name","code"]
    list_editable = ["name"]
    radio_fields = {"status": admin.VERTICAL}
    search_fields = ('name', 'status')
    list_filter = (ProductFilter,)
    ordering = ('-date_creation',)
    actions = [set_product_online, set_product_offline]
    # def tax(self, instance):
    #     return (instance.price_ttc / instance.price_ht)-1
    # tax.short_description = "Taxes (%)"

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Commande)

# Register your models here.
