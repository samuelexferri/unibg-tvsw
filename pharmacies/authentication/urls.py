from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy, include
from rest_framework import routers

from authentication import views

app_name = 'authentication'

router = routers.DefaultRouter()
router.register(r'user/api', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.homepage, name='home'),
    path(r'', include(router.urls)),
    path('register/', views.signup, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html',
                                              email_template_name='authentication/password_reset_email.html',
                                              success_url=reverse_lazy('authentication:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html',
                                                     success_url=reverse_lazy('authentication:password_reset_complete')
                                                     ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
]
