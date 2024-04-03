from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name="login"),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('upload/', views.upload_video, name='upload_video'),
    path('profile/', views.profile_page, name='profile_page'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='password_reset_complete'),
    path('about-us/', views.aboutus, name="about-us"),
    path('delete/<int:item_id>/', views.delete_entry, name='delete_entry'),
]
