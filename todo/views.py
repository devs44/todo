from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from dashboard.models import Todo, TodoUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings as conf_settings


from .forms import (
    TodoForm, TodoRegisterForm, 
    TodoLoginForm, 
    TodoUserPasswordResetForm, 
    TodoUserChangePasswordForm)
from .mixin import (
    TodoLoginRequiredMixin, 
    DeleteMixin)

# Create your views here.
class TodoRegisterView(CreateView):
    template_name = 'todo/auth/register.html'
    form_class = TodoRegisterForm
    success_url = reverse_lazy('todo:todo-login')

    def form_valid(self, form):        
        user = TodoUser.objects.create(
            username=form.cleaned_data.get('username'), 
            first_name=form.cleaned_data.get('first_name'), 
            last_name=form.cleaned_data.get('last_name'), 
            email = form.cleaned_data.get('email')
        )
        
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        messages.success(self.request,"User Sucessfully created")

        login(self.request, user)
        return redirect(self.success_url)


class TodoLoginView(FormView):
    form_class = TodoLoginForm
    template_name = 'todo/auth/login.html'
    success_url = reverse_lazy('todo-todo')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        login(self.request, user)
        
        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('todo:todo')


class TodoLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('todo:todo-login')


class TodoForgotPassword(FormView):
    template_name = 'todo/auth/reset-password.html'
    form_class = TodoUserPasswordResetForm
    success_url = reverse_lazy('todo:todo-login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        password = get_random_string(8)
        user.set_password(password)
        user.save(update_fields=['password'])

        text_content = 'Your password has been changed. {} '.format(password)
        send_mail(
            'Password Reset | Todo',
            text_content,
            conf_settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(self.request, "Password reset code is sent")
        return super().form_valid(form)

class TodoChangePassword(PasswordChangeView):
    
    template_name = 'todo/auth/password-change.html'
    form_class = TodoUserChangePasswordForm
    success_url = reverse_lazy('todo:todo-login')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form
       

class TodoView(TodoLoginRequiredMixin, ListView):
    template_name = 'todo/base/list.html'
    model = Todo
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['todo'] = Todo.objects.filter(deleted_at__isnull=True, user=self.request.user)
        return context

class TodoTableView(TodoLoginRequiredMixin, ListView):
    template_name = 'todo/base/table.html'
    model = Todo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = Todo.objects.filter(deleted_at__isnull=True, user=self.request.user)
        return super().get_context_data(**kwargs)


class TodoDetailView(TodoLoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/base/detail.html'
    context_object_name = 'detail'

class TodoCreateView(TodoLoginRequiredMixin, CreateView):
    template_name = 'todo/base/form.html'
    form_class = TodoForm
    success_url = reverse_lazy('todo:todo')

    def form_valid(self, form):
        user = TodoUser.objects.get(username = self.request.user)
        form.instance.user = user
        messages.success(self.request,"Todo Sucessfully created")
        return super().form_valid(form)


class TodoUpdateView(TodoLoginRequiredMixin, UpdateView):
    template_name = 'todo/base/form.html'
    form_class = TodoForm
    model =Todo
    success_url = reverse_lazy('todo:todo')

class TodoDeleteView(TodoLoginRequiredMixin,DeleteMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todo:todo')
    


