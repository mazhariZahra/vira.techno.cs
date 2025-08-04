from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('orders/', views.order_list, name='order_list'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('get-order-form/<int:service_id>/', views.get_order_form, name='get_order_form'),
    path('cart/', views.cart_view, name='cart'),
    path('payment-process/', views.payment_process, name='payment_process'),
    path('profile/', views.profile_view, name='profile'),
    path('send-message/', views.send_message, name='send_message'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('faq/', views.faq, name='faq'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('',views.home_view, name='home'),
]