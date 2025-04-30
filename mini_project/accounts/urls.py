from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Get_Started, name='Get_Started'),
    path('login_signup/', views.login_signup, name='login_signup'),
    path('Otp/', views.Otp, name='Otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password_form/', views.reset_password_form, name='reset_password_form'),
    path('home/', views.home, name='home'), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
