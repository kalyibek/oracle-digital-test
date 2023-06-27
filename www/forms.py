from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from . import models


class RegistrationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        group = Group.objects.get(name='Teacher')

        if commit:
            user.save()
            user.groups.add(group)

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2', 'phone_number')


class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ('fio', 'email', 'birth_date',
                  'klass', 'address', 'sex', 'photo')


class SearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=255)


class MailingForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)

