from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Update Profile with Phone and Address
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            image = form.cleaned_data.get('image')
            if hasattr(user, 'profile'):
                user.profile.phone = phone
                user.profile.address = address
                if image:
                    user.profile.image = image
                user.profile.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. Continue to Log in')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)

def register_admin(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            # Update Profile with Phone and Address
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            image = form.cleaned_data.get('image')
            if hasattr(user, 'profile'):
                user.profile.phone = phone
                user.profile.address = address
                if image:
                    user.profile.image = image
                user.profile.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Admin account has been created for {username}. Continue to Log in')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register_admin.html', context)


def profile(request):
    return render(request, 'user/profile.html')

def profile_update(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request, 'user/profile_update.html', context)

from django.contrib.auth import login
from django.contrib.auth.models import User

def farmer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            user = User.objects.filter(email=email).first()
            if user:
                if hasattr(user, 'profile') and user.profile.phone == phone:
                    login(request, user)
                    if user.is_staff:
                        return redirect('dashboard-index')
                    return redirect('farmer-orders')
                else:
                    messages.error(request, 'Invalid Mobile Number')
            else:
                messages.error(request, 'User with this email not found')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'user/farmer_login.html')