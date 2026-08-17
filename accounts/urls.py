from django.urls import path
from . import views
from .views import ( CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, )

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'profile/change-password/',
        views.change_password,
        name='change_password'
    ),

    path(
        'password-reset/',
        CustomPasswordResetView.as_view(),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]