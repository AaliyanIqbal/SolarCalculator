from django.contrib import admin
from .models import UserDetail
from .models import Quote

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number')  # Fields to display in the admin list view
    search_fields = ('name', 'email', 'number')  # Fields to search by in the admin interface


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'panels_required_pdf' ,'house_consumption_pdf','battries_required_pdf','required_inverter_pdf', 'solar_kw_production', 'battery_kw_production', 'panel_pricing', 'battery_pricing', 'inverter_pricing', 'total_cost')
    list_filter = ('user',)
    search_fields = ('user__name', 'user__email', 'user__number')

# Register the Quote model with the custom admin class
admin.site.register(Quote, QuoteAdmin)