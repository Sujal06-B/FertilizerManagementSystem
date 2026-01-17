def register_admin(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            # Update Profile if needed
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
