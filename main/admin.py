from django.contrib import admin
from .models import Service, Order ,ServiceCard ,Slider, Profile,About,Contact,ContactMessage,CustomOrderField,ChatMessage,Stat,TermsAndConditions,FAQ
# Register your models here.
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(ContactMessage)
admin.site.register(ServiceCard)
admin.site.register(ChatMessage)
admin.site.register(Stat)
admin.site.register(TermsAndConditions)
admin.site.register(FAQ)
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ['order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'description','base_price')
    list_filter = ('icon_class',)
    search_fields = ('title', 'description')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'updated_at')
    search_fields = ('user__username', 'full_name', 'phone_number')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'service', 'custom_service', 'total_price', 'status', 'date_ordered', 'has_file')  # اضافه کردن has_file برای نمایش وجود فایل
    list_filter = ('service', 'status', 'date_ordered')
    search_fields = ('full_name', 'phone_number', 'description', 'custom_service', 'service__title', 'admin_note')  # اضافه کردن admin_note به جستجو
    readonly_fields = ('date_ordered',)

    # متد برای نمایش وجود فایل
    def has_file(self, obj):
        return bool(obj.file_upload)
    has_file.short_description = 'فایل موجود است'
    has_file.boolean = True  # نمایش به‌صورت تیک یا ضربدر

    # فیلدهای قابل ویرایش تو فرم ادمین
    fields = ('user', 'service', 'custom_service', 'full_name', 'phone_number', 'description', 'file_upload', 'admin_note', 'total_price', 'status')

@admin.register(CustomOrderField)
class CustomOrderFieldAdmin(admin.ModelAdmin):
    list_display = ('service', 'field_name', 'field_type', 'is_required', 'price_per_unit')
