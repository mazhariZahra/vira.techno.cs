from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ServiceCard ,Slider, Order, Service, Profile, About, Contact,ContactMessage,CustomOrderField,ChatMessage,Stat,TermsAndConditions,FAQ

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # فرض می‌کنیم در فرم نام کاربری هست
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید.')
            return render(request, 'main/register.html')

        if password1 != password2:
            messages.error(request, 'رمز عبور و تکرارش مطابقت ندارند.')
            return render(request, 'main/register.html')

        # اگر یوزر وجود داشت
        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً ثبت شده است.')
            return render(request, 'main/register.html')

        # ایجاد کاربر جدید
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد. اکنون وارد شوید.')
        return redirect('login')  # این نام باید در urls.py تعریف شده باشد

    return render(request, 'main/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'main/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'کاربری با این ایمیل یافت نشد')
        else:
            messages.success(request, 'در صورت وجود ایمیل در سیستم، لینک بازیابی ارسال شد')
        return redirect('forgot_password')
    return render(request, 'main/forgot-password.html')

def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'رمز عبورها یکسان نیستند')
        else:
            # اینجا در واقع باید از توکن استفاده کنی و کاربر رو شناسایی کنی
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
            return redirect('login')

    return render(request, 'main/reset-password.html')


def home_view(request):
    cards = ServiceCard.objects.all()
    sliders = Slider.objects.all().order_by('order')
    stats = Stat.objects.all()
    recommendations = []
    # منطق پیشنهاد هوشمند فقط برای کاربرهای واردشده
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).values_list('service_id', flat=True)
        if user_orders:
            related_services = ServiceCard.objects.exclude(id__in=user_orders).order_by('?')[:3]
            for card in related_services:
                recommendations.append({
                    'title': card.title,
                    'description': card.description,
                    'icon_class': card.icon_class,
                    'order_link': reverse('order_list') + f'?service={card.id}'
                })
    return render(request, 'main/home.html', {
        'cards': cards,
        'sliders': sliders,
        'recommendations': recommendations,
        'stats': stats
    })

def order_list(request):
    services = Service.objects.all()  # مطمئن شو دیتابیس سرویس داره
    return render(request, 'main/orders.html', {'services': services})

def get_order_form(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        custom_fields = CustomOrderField.objects.filter(service=service).values('id', 'field_name', 'field_type', 'is_required', 'price_per_unit')
        total_price = service.base_price  # قیمت پایه
        return JsonResponse({'custom_fields': list(custom_fields), 'total_price': float(total_price), 'service_title': service.title})
    except Service.DoesNotExist:
        return JsonResponse({'error': 'خدمت یافت نشد'}, status=404)

def submit_order(request):
    if request.method == 'POST':
        # اینجا باید داده‌ها رو ذخیره کنی (مثلاً تو مدل Order)
        messages.success(request, 'سفارش با موفقیت ثبت شد!')
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'درخواست نامعتبر'}, status=400)

def login_view(request):
    if request.method == 'POST':
        if 'login-username' in request.POST:
            username = request.POST.get('login-username')
            password = request.POST.get('login-password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود با موفقیت انجام شد!')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
                return render(request, 'main/login.html')
        elif 'register-username' in request.POST:
            username = request.POST.get('register-username')
            email = request.POST.get('register-email')
            password = request.POST.get('register-password')
            full_name = request.POST.get('register-full_name')
            phone_number = request.POST.get('register-phone_number')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'این نام کاربری قبلاً ثبت شده است.')
                return render(request, 'main/login.html')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
                return render(request, 'main/login.html')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            if full_name or phone_number:
                profile = Profile(user=user, full_name=full_name, phone_number=phone_number)
                profile.save()

            messages.success(request, 'ثبت‌نام با موفقیت انجام شد! لطفاً وارد شوید.')
            return redirect('login')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید!')
    return render(request, 'main/logout.html')

def about(request):
    about_content = About.objects.first()
    return render(request, 'main/about.html', {'about_content': about_content})

def contact(request):
    contact_info = Contact.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, f'پیام شما از {name} با موفقیت ثبت شد!')
        else:
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید.')
    return render(request, 'main/contact.html', {'contact_info': contact_info})

def get_custom_fields(request):
    service_title = request.GET.get('service')
    if service_title == 'سایر':
        return JsonResponse({'custom_fields': [], 'total_price': 0})
    try:
        service = Service.objects.get(title=service_title)
        custom_fields = list(CustomOrderField.objects.filter(service=service).values('field_name', 'field_type', 'is_required'))
        total_price = service.base_price
        return JsonResponse({'custom_fields': custom_fields, 'total_price': float(total_price)})
    except Service.DoesNotExist:
        return JsonResponse({'custom_fields': [], 'total_price': 0})
    
def cart_view(request):
    cart = request.GET.get('cart')
    if cart:
        cart_data = json.loads(request.GET.get('cart'))
    else:
        cart_data = json.loads(request.session.get('cart', '[]'))
    return render(request, 'main/cart.html', {'cart': cart_data})

def payment_process(request):
    if request.method == 'GET':
        amount = request.GET.get('amount')
        cart = request.GET.get('cart')
        if amount and cart:
            try:
                cart_data = json.loads(cart)
                total = sum(float(item['totalPrice'].replace(' تومان', '')) for item in cart_data if item.get('totalPrice'))
                return render(request, 'main/payment.html', {
                    'amount': amount,
                    'cart': cart_data,
                    'total': total
                })
            except json.JSONDecodeError:
                return render(request, 'main/error.html', {'message': 'داده‌های سبد خرید نامعتبر است.'})
        return render(request, 'main/error.html', {'message': 'خطا در پردازش پرداخت.'})
    return render(request, 'main/error.html', {'message': 'متد درخواست نامعتبر است.'})

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        user = request.user

        # دریافت داده‌های فرم
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        full_name = request.POST.get('full_name', profile.full_name)
        phone_number = request.POST.get('phone_number', profile.phone_number)
        password = request.POST.get('password')

        # چک کردن رمز عبور برای تأیید
        if password:
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is None:
                messages.error(request, 'رمز عبور فعلی اشتباه است.')
                return render(request, 'main/profile.html', {
                    'profile': profile,
                    'orders': Order.objects.filter(user=request.user).order_by('-date_ordered')
                })

            # به‌روزرسانی نام کاربری و ایمیل
            user.username = username
            user.email = email
            user.save()
            update_session_auth_hash(request, user)  # به‌روزرسانی سشن بعد از تغییر

        # به‌روزرسانی پروفایل
        profile.full_name = full_name
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')
        return redirect('profile')

    return render(request, 'main/profile.html', {
        'profile': request.user.profile,
        'orders': Order.objects.filter(user=request.user).order_by('-date_ordered')
    })

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            chat = ChatMessage.objects.create(user=request.user, message=message)
            return JsonResponse({'status': 'success', 'message': 'پیام شما با موفقیت ذخیره شد'})
        return JsonResponse({'status': 'error', 'message': 'پیام خالی است'})
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})

def terms_and_conditions(request):
    terms = TermsAndConditions.objects.first()  # فرض می‌کنیم فقط یه رکورد داریم
    return render(request, 'main/terms_and_conditions.html', {'terms': terms})

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/password_reset_email.html'  # قالب سفارشی ایمیل
    success_url = '/password-reset/done/'  # بعد از ارسال لینک

    def form_valid(self, form):
        messages.success(self.request, 'لینک بازیابی به ایمیل شما ارسال شد.')
        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = '/reset/done/'

    def form_valid(self, form):
        messages.success(self.request, 'رمز عبور شما با موفقیت تغییر کرد.')
        return super().form_valid(form)

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'