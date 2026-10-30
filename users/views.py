from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ProfileForm, UserForm


def register(request):
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}. You can now log in.")
            return redirect("users:login")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            next_url = request.POST.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})

@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("posts:home")

@login_required
def profile(request):
    return render(request, "users/profile.html", {"profile": request.user.profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    old_avatar = profile.avatar.name

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_ok = user_form.is_valid()
        profile_ok = profile_form.is_valid()

        if user_ok and profile_ok:
            try:
                user_form.save()
                profile_form.save()
            except OSError:
                messages.error(request, "We could not save your changes. Please try again later.")
            else:
                new_avatar = profile.avatar.name
                if old_avatar and old_avatar != new_avatar:
                    try:
                        profile.avatar.storage.delete(old_avatar)
                    except OSError:
                        pass
                messages.success(request, "Your profile has been updated.")
                return redirect("users:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {"user_form": user_form, "profile_form": profile_form})
