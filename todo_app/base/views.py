from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# reverse_lazy odpowiada za przekierowanie na podstronę
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
# LoginRequiredMixin odpowiada za wymaganie zalogowania do wyświetlania szablonów przez konkretne viewsy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


# LoginView odpowiada za automatyczne wygenerowanie formularza służącego do logowania
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# W django nie ma wbudowanego View dla rejestracji, więc w tym celu wykrozystany został FormView, który odpowiada
# za wyświetlenie formularza UserCreationForm, który jest odpowiedzialny za tworzenie użytkownika
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # Nadpisanie metody form_valid, aby po zarejestrowaniu użytkownik automatycznie był logowany
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # Napisanie metody get, aby zalogowany użytkownik nie mógłwejść na podstronę rejestracji
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# ListView odpowiada za zwrócenie informacji o elementach z bazy danych w postaci listy. Automatycznie szuka szablonu
# o nazwie "'nazwa_klasy.model.wartość'_list.html"
class TaskList(LoginRequiredMixin, ListView):
    # Jako model wykorzystujemy nasz model zadania
    model = Task
    # Zmiana nazwy z 'object_list' (wykorzystywane w szablonach) na 'tasks'
    context_object_name = 'tasks'

    # Nadpisanie metody w celu wyświetlania użytkownikowi tylko jego zadań, poprzez filter, a następnie przekazanie
    # ich jako context, w którym przekazujemy także liczbę zadań danego użytkownika. Zmienna context jest przekazywana
    # do konkretnego szablonu, w którym możemy wykorzystać te dane
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


# DetailView odpowiada za zwracanie informacji o pojedynczym elemencie. Automatycznie szuka szablonu
# o nazwie "'nazwa_klasy.model.wartość'_detail.html"
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    # Zmiana nazwy z 'object' (wykorzystywane w szablonach) na 'task'
    context_object_name = 'task'
    # Zmiana nazwy dla automatycznie szukanego szablonu
    template_name = 'base/task.html'


# CreateView odpowiada za wysłanie zapytania typu POST tworzącego w bazie nasze zadanie, poprzez automatyczne
# wygenerowanie formularza
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # Wyświetlamy wszystkie pola oprócz pola user, który dzięki poniższej metodzie jest przydzielany automatycznie
    fields = ['title', 'description', 'complete']
    # Ustawiamy przekierowanie po utworzeniu zadania
    success_url = reverse_lazy('tasks')

    # Nadpisanie metody form_valid, aby konkretny użytkownik mógł dodawać zadania tylko dla siebie
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


# UpdateView odpowiada za edycję elementu w bazie danych
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    # Nadpisanie metody form_valid, aby konkretny użytkownik mógł edytować zadania tylko dla siebie
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)


# DeleteView odpowiada za usunięcie elementu z bazy danych.
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    fields = '__all__'
    success_url = reverse_lazy('tasks')
