from datetime import datetime

import cloudinary.uploader
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from config import settings
from vagas.forms import VagasForm, CandidaturaForm
from .models import Vagas, Candidatura


class VagasListView(ListView):
    model= Vagas
    template_name='vagas/vagas_list.html'
    context_object_name= 'vagas'

class VagasCreateView(CreateView):
    model = Vagas
    form_class = VagasForm
    template_name = 'vagas/vagas_form.html'
    success_url = reverse_lazy('vagas-list')

class VagasUpdateView(UpdateView):
    model = Vagas
    form_class = VagasForm
    template_name = 'vagas/vagas_form.html'
    success_url = reverse_lazy('vagas-list')

class VagasDeleteView(DeleteView):
    model = Vagas
    template_name = 'vagas/vagas_confirm_delete.html'
    success_url = reverse_lazy('vagas-list')

class CandidaturasCreateView(View):
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


# Create your views here.
