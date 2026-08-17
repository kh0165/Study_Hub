from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from django.contrib.auth.views import ( PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, )

def home(request):
    return render(request, 'accounts/home.html')


def register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            return render(
                request,
                'accounts/register.html',
                {'error': 'This email is already registered.'}
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        Profile.objects.create(user=user)

        login(request, user)

        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        return render(
            request,
            'accounts/login.html',
            {'error': 'Invalid email or password.'}
        )

    return render(request, 'accounts/login.html')


def logout_view(request):

    logout(request)

    return redirect('home')


@login_required
def dashboard(request):

    profile = request.user.profile

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'profile': profile,
        }
    )


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        request.user.first_name = name
        request.user.email = email
        request.user.username = email

        request.user.save()

        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        return redirect('profile')

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'profile': profile,
        }
    )


@login_required
def change_password(request):

    if request.method == 'POST':

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            return render(
                request,
                'accounts/change_password.html',
                {
                    'error': 'Current password is incorrect.'
                }
            )

        if new_password != confirm_password:
            return render(
                request,
                'accounts/change_password.html',
                {
                    'error': 'New passwords do not match.'
                }
            )

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return redirect('profile')

    return render(
        request,
        'accounts/change_password.html'
    )


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/password-reset/done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/password-reset-complete/'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'