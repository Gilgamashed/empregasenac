from django.contrib import messages
from django.shortcuts import redirect

from vagas.models import Empresa


class EmpresaRequiredMixin:
    """ Mixin para restringir acesso a usuários com perfil de Empresas."""

    def dispatch(self, request, *args, **kwargs):
        empresa = Empresa.objects.filter(user=self.request.user).first()
        if not empresa:
            messages.error(self.request, "Apenas empresas logadas são autorizadas à cadastrar vagas.")
            return redirect('home')
        request.empresa_logada = empresa
        return super().dispatch(request, *args, **kwargs)