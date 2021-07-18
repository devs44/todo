from django.urls import path
 

from . import views

app_name = 'todo'

urlpatterns=[       
        path('', views.TodoView.as_view(), name='todo'),
        path('todo/table/', views.TodoTableView.as_view(), name='todo-table'),

        path('todo/create/', views.TodoCreateView.as_view(), name='todo-create'),
        path('todo/<int:pk>/update', views.TodoUpdateView.as_view(), name='todo-update'),
        path('todo/<int:pk>/detail', views.TodoDetailView.as_view(), name='todo-detail'),
        path('todo/<int:pk>/delete', views.TodoDeleteView.as_view(), name='todo-delete'),

        path('todo/register', views.TodoRegisterView.as_view(), name='todo-register'),
        path('todo/login', views.TodoLoginView.as_view(), name='todo-login'),
        path('todo/logout', views.TodoLogoutView.as_view(), name='todo-logout'),
        
        path('todo/users/forogot-password', views.TodoForgotPassword.as_view(), name='todo-forgot-password'),
        path('todo/users/change-password', views.TodoChangePassword.as_view(), name='todo-change-password'),
]