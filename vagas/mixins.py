from django.contrib import messages
from django.shortcuts import redirect

from vagas.models import Empresa, Vagas, Candidato


class EmpresaRequiredMixin:
    """ Mixin para restringir acesso a usuários com perfil de Empresas."""

    def dispatch(self, request, *args, **kwargs):
        empresa = Empresa.objects.filter(user=self.request.user).first()
        if not empresa:
            messages.error(self.request, "Apenas empresas logadas são autorizadas à cadastrar vagas.")
            return redirect('home')
        request.empresa_logada = empresa
        return super().dispatch(request, *args, **kwargs)

class VagasOwnerMixin:
    """ Mixin para que vagas sejam modificadas apenas por seus criadores
        Deve ser usado com views que recebem pk como parametro.
    """

    def dispatch(self, request, *args, **kwargs):
        vaga = Vagas.objects.filter(pk=kwargs.get('pk'), empresa=request.empresa_logada).first()
        if not vaga:
            messages.error(request, "Vagas podem ser gerenciadas apenas por seus criadores")
            return redirect('vagas-list')
        return super().dispatch(request, *args, **kwargs)

class CandidatoRequiredMixin:
    """ Mixin para restringir canditação de empresas à vagas"""

    def dispatch(self, request, *args, **kwargs):

        if not Candidato.objects.filter(user=request.user).exists():
            messages.error(self.request, "Empresas não podem se candidatar a vagas")
            return redirect('vagas-list')
        return super().dispatch(request, *args, **kwargs)