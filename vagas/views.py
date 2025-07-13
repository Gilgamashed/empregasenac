from datetime import datetime

import cloudinary.uploader
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView

from config import settings
from vagas.forms import VagasForm, CandidaturaForm, CandidatoSignUpForm, EmpresaSignUpForm
from .models import Vagas, Candidatura, Candidato, Empresa


class VagasListView(ListView):
    model= Vagas
    template_name='vagas/vagas_list.html'
    context_object_name= 'vagas'

class VagasCreateView(LoginRequiredMixin,CreateView):
    model = Vagas
    form_class = VagasForm
    template_name = 'vagas/vagas_form.html'
    success_url = reverse_lazy('vagas-list')

class VagasUpdateView(LoginRequiredMixin,UpdateView):
    model = Vagas
    form_class = VagasForm
    template_name = 'vagas/vagas_form.html'
    success_url = reverse_lazy('vagas-list')

class VagasDeleteView(LoginRequiredMixin,DeleteView):
    model = Vagas
    template_name = 'vagas/vagas_confirm_delete.html'
    success_url = reverse_lazy('vagas-list')

class CandidaturasCreateView(LoginRequiredMixin,View):
    def get(self, request, vaga_id):
        form = CandidaturaForm()
        return render(request, 'vagas/candidatura_form.html', {'form': form})

    def post(self, request, vaga_id):
        form = CandidaturaForm(request.POST, request.FILES)
        vaga = get_object_or_404(Vagas, id=vaga_id)
        if form.is_valid():
            Candidatura.objects.create(
                vaga=vaga,
                nome=form.cleaned_data.get('nome'),
                email=form.cleaned_data.get('email'),
                curriculo=form.cleaned_data.get('curriculo'),
            )

            date_prefix = datetime.now().strftime('%Y_%m_%d')
            filename = f'{date_prefix}_curriculo_{form.cleaned_data.get('nome')}'

            cloudinary.uploader.upload(
                file=form.cleaned_data.get('curriculo'),
                asset_folder='curriculos',
                public_id=filename,
                override=True,
                resource_type="raw"
            )

            send_mail(
                subject='Confirmação de candidatura',
                message=f'Olá {form.cleaned_data.get('nome')}, sua candidatura foi recebida!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data.get('email')],
                fail_silently=True,
            )

            return redirect('vagas-list')
        return render(request,'vagas/candidatura_form.html', {'form':form})


class CandidatoSignUpView(CreateView):
    model = User
    form_class = CandidatoSignUpForm
    template_name = "registration/signup_candidato.html"
    success_url = reverse_lazy('vagas-list') #TODO: mudar para página de home

    def form_valid(self, form):
        response = super().form_valid(form)
        Candidato.objects.create(
            user=self.object,
            nome= form.cleaned_data.get('nome'),
            telefone= form.cleaned_data.get('telefone'),
            cidade= form.cleaned_data.get('cidade'),
        )
        login(self.request, self.object)
        return response


class EmpresaSignUpView(CreateView):
    model = User
    form_class = EmpresaSignUpForm
    template_name = "registration/signup_empresa.html"
    success_url = reverse_lazy('vagas-list')  # TODO: mudar para página de home

    def form_valid(self, form):
        response = super().form_valid(form)
        Empresa.objects.create(
            user=self.object,
            nome_empresa=form.cleaned_data.get('nome_empresa'),
            cnpj=form.cleaned_data.get('cnpj'),
        )
        login(self.request, self.object)
        return response


class HomeView(TemplateView):
    template_name = "vagas/home.html"



# Create your views here.
