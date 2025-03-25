from django.contrib import admin
from .models import User,CartItem



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'name', 'is_active', 'is_staff')
    search_fields = ('phone', 'email', 'name')
    list_filter = ('is_active', 'is_staff')
    inlines = [CartItemInline]