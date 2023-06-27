from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.StudentsListView.as_view(), name='index'),
    path('student-create/', views.StudentCreateView.as_view(), name='student-create'),
    path('student-detail/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('student-update/<int:pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('student-delete/<int:pk>/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('mailing/', views.mailing, name='mailing'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
