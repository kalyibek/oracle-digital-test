from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from .signals import send_email_on_user_creation
from . import forms
from . import models


def is_passed_test(user):
    return user.is_superuser or user.groups.filter(name='Teacher').exists()


class StudentsListView(UserPassesTestMixin, generic.ListView):
    model = models.Student
    template_name = 'www/index.html'
    context_object_name = 'students'
    login_url = '/login/'

    def test_func(self):
        return is_passed_test(self.request.user)


class StudentCreateView(UserPassesTestMixin, generic.CreateView):
    model = models.Student
    template_name = 'www/student_create.html'
    fields = ('fio', 'email', 'birth_date',
              'klass', 'address', 'sex', 'photo')
    success_url = reverse_lazy('index')

    def test_func(self):
        return is_passed_test(self.request.user)

    def form_valid(self, form):
        send_email_on_user_creation(sender=self.model,
                                    instance=form.instance, created=True)
        return super().form_valid(form)


class StudentDetailView(UserPassesTestMixin, generic.DetailView):
    model = models.Student
    template_name = 'www/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        return is_passed_test(self.request.user)


class StudentUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = models.Student
    template_name = 'www/student_update.html'
    fields = ('fio', 'email', 'birth_date',
              'klass', 'address', 'sex', 'photo')
    context_object_name = 'student'

    def test_func(self):
        return is_passed_test(self.request.user)

    def get_success_url(self):
        return reverse_lazy('student-detail', kwargs={'pk': self.object.pk})


class StudentDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = models.Student
    template_name = 'www/student_delete.html'
    success_url = reverse_lazy('index')
    context_object_name = 'student'

    def test_func(self):
        return is_passed_test(self.request.user)


class SearchView(UserPassesTestMixin, generic.ListView):
    model = models.Student
    template_name = 'www/index.html'
    context_object_name = 'students'
    form_class = forms.SearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(fio__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.SearchForm()
        return context

    def test_func(self):
        return is_passed_test(self.request.user)


@login_required(login_url='/login/')
def mailing(request):
    if request.method == 'POST':
        form = forms.MailingForm(request.POST)

        if form.is_valid():
            email_list = models.Student.objects.values_list('email', flat=True)

            send_mail(
                subject='School',
                message=form.cleaned_data['text'],
                from_email='kenwaynoreply@yandex.ru',
                recipient_list=email_list
            )
            return redirect(reverse('index'))

    form = forms.MailingForm()
    return render(request, 'www/mailing.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))

    form = forms.RegistrationForm()
    return render(request, 'www/register.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            return render(request, 'www/login.html', {'error': 'Неверные учетные данные'})

    return render(request, 'www/login.html')
