"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import home, about, add_student, add_invoice, add_lesson, edit_invoice, delete_invoice, student_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name= 'home'),
    path('about/', about, name= 'about'),
    path('add_student/', add_student, name='add_student'),
    path('add_invoice/', add_invoice, name ='add_invoice'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_lesson/', add_lesson, name='add_lesson'),

    path('invoice/edit/<int:pk>/', edit_invoice, name='edit_invoice'),
    path('invoice/delete/<int:pk>/', delete_invoice, name='delete_invoice'),
    path('student/<int:pk>/', student_detail, name='student_detail'),
]
