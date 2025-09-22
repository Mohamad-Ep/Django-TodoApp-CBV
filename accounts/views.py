from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterUserForm, LoginUserForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# ________________________________________________


class RegisterUserView(View):
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todos:todolist')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            CustomUser.objects.create_user(
                email=data['email'], password=data['password1']
            )
            messages.success(request, 'ثبت نام کاربر با موفقیت ایجاد شد')
            return redirect('accounts:login')

        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name, {'form': form})


# ________________________________________________


class LoginUserView(View):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todos:todolist')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['email'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'ورود با موفقیت انجام شد')
                    next_page = request.GET.get('next')
                    if next_page is not None:
                        return redirect(next_page)
                    return redirect('todos:todolist')
                else:
                    messages.warning(request, 'کاربر غیرفعال میباشد')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.warning(request, 'کاربری با این مشخصات یافت نشد')
                return render(request, self.template_name, {'form': form})
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
                return render(request, self.template_name, {'form': form})


# ________________________________________________


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('todos:index')


# ________________________________________________
