from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    ICON_CHOICES = [
        ('fa-keyboard', 'تایپ'),
        ('fa-tools', 'تعمیرات'),
        ('fa-user-plus', 'ثبت‌نام'),
        ('fa-file-alt', 'ترجمه'),
        ('fa-code', 'برنامه‌نویسی'),
        ('fa-paint-brush', 'طراحی گرافیک'),
        ('fa-laptop', 'لپ‌تاپ'),
        ('fa-server', 'سرور'),
        ('fa-database', 'دیتابیس'),
        ('fa-print', 'پرینت'),
        ('fa-camera', 'عکاسی'),
        ('fa-video', 'فیلم‌برداری'),
        ('fa-mobile-alt', 'موبایل'),
        ('fa-cogs', 'تنظیمات'),
        ('fa-network-wired', 'شبکه'),
        ('fa-cloud', 'کلود'),
        ('fa-bug', 'دیباگ'),
        ('fa-shield-alt', 'امنیت'),
        ('fa-file-excel', 'اکسل'),
        ('fa-file-word', 'وورد'),
        ('fa-file-powerpoint', 'پاورپوینت'),
        ('fa-photo-video', 'چندرسانه‌ای'),
        ('fa-globe', 'وب‌سایت'),
        ('fa-shopping-cart', 'فروشگاه آنلاین'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, choices=ICON_CHOICES, blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # اصلاح شده

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    custom_service = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    description = models.TextField(blank=True)
    file_upload = models.FileField(upload_to='orders/', null=True, blank=True)
    admin_note = models.TextField(blank=True, verbose_name='توضیحات ادمین')  # فیلد جدید
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'در انتظار'),
            ('processing', 'در حال پردازش'),
            ('completed', 'کامل'),
        ],
        default='pending'
    )

    def __str__(self):
        service_name = self.custom_service if self.custom_service else self.service.title if self.service else 'Unknown'
        return f"{self.full_name or 'Unknown'} - {service_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class ServiceCard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50)  # مثلاً 'fas fa-code'
    order_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Slider(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sliders/')
    order = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class About(models.Model):
    content = models.TextField(verbose_name="محتوای درباره ما")

    def __str__(self):
        return "درباره ما"

# مدل جدید برای ارتباط با ما
class Contact(models.Model):
    address = models.TextField(verbose_name="آدرس")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")

    def __str__(self):
        return "ارتباط با ما"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پیام از {self.name} - {self.date_sent}"

class CustomOrderField(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # اسم فیلد (مثلاً "تعداد صفحات")
    field_type = models.CharField(max_length=50, choices=[('text', 'متن'), ('number', 'عدد'), ('file', 'فایل')], default='text')  # نوع فیلد
    is_required = models.BooleanField(default=True)  # اجباری یا اختیاری
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # قیمت اضافی بر اساس مقدار

    def __str__(self):
        return f"{self.field_name} برای {self.service.title}"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
    
class Stat(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=20)  # مثل "+50k" یا "100%"
    icon_class = models.CharField(max_length=50, help_text="مثلاً: fas fa-users")

    def __str__(self):
        return self.title
    
class TermsAndConditions(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question