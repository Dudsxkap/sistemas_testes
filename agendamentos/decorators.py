from django.shortcuts import redirect
from agendamentos.models import Cidadao


def cidadao_required():
    def decorator(func, **args):
        def newfn(request, **kwargs):
            if request.user.is_authenticated:
                if not Cidadao.objects.filter(auth_user=request.user).exists():
                    return redirect('login')
            else:
                return redirect('login')
            return func(request, **kwargs)
        return newfn
    return decorator


def apto_agendamento_required():
    def decorator(func, **args):
        def newfn(request, **kwargs):
            if request.user.is_authenticated:
                if not request.user.cidadao.apto_agendamento:
                    return redirect('index')
            else:
                return redirect('login')
            return func(request, **kwargs)
        return newfn
    return decorator
