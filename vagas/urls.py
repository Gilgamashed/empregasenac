"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from vagas import views
from vagas.views import CandidatoSignUpView, EmpresaSignUpView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("vagas", views.VagasListView.as_view(), name='vagas-list'),
    path('vagas/nova/', views.VagasCreateView.as_view(), name='vagas-create'),
    path('vagas/<int:pk>/editar/', views.VagasUpdateView.as_view(), name='vagas-update'),
    path('vagas/<int:pk>/excluir/', views.VagasDeleteView.as_view(), name='vagas-delete'),
    path('candidatar/<int:vaga_id>/', views.CandidaturasCreateView.as_view(), name='candidatar'),
]

urlpatterns += [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/candidato/',CandidatoSignUpView.as_view(), name='signup_candidato'),
    path('signup/empresa/', EmpresaSignUpView.as_view(), name='signup_empresa'),
]