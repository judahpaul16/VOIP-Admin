from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render

class LoginView(auth_views.LoginView):
    template_name = "login.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return HttpResponseRedirect(reverse("dashboard"))

class LoginRedirectView(auth_views.LoginView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return HttpResponseRedirect("login")

    def get_success_url(self):
        return HttpResponseRedirect(reverse("dashboard"))

def register_view(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account was successfully created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {'form': form})

@login_required
def profile_view(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            person = request.user.first_name
            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
