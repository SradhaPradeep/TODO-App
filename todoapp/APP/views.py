from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView,ListView, DetailView, UpdateView, DeleteView
from.models import Tasks
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = '/task/'

    def get_success_url(self):
        return super().get_success_url()
    
    
class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm  # Corrected attribute name
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # Corrected method name

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('createtask')
        return super().get(*args, **kwargs)

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Tasks
    fields = ['task','completed','description']
    success_url = reverse_lazy('task')
    template_name = 'task_create.html'
    
    def form_valid(self, form):
         form.instance.user = self.request.user
         return super().form_valid(form)
    
    
class TaskList(LoginRequiredMixin,ListView):
    model = Tasks
    context_object_name = 'task'
    template_name= 'task_list.html'
    
    def get_queryset(self): 
        return Tasks.objects.filter(user=self.request.user)

    
class TaskDetailView(DetailView):
    model = Tasks
    
    template_name = 'task_details.html'
    
        
class TaskUpdate(UpdateView):
    model = Tasks
    fields = ['task','completed','description']
    success_url = reverse_lazy('task')
    template_name = 'task_create.html'
        
       
class TaskDelete(DeleteView):
    model = Tasks
  
    success_url = reverse_lazy('task')
    template_name = 'task_delete.html'
    