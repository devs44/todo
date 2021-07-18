from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class TodoLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('todo:todo-login')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_superuser or self.request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class DeleteMixin(object):
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)