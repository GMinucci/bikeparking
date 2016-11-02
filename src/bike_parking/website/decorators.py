from django.shortcuts import redirect
from six import wraps
from parking.models import Person


def user_or_admin(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('usuario-resumo')
        if not request.user.groups.filter(name='admin').exists():
            try:
                person = Person.objects.get(user=request.user)
                if person.cpf is "":
                    return redirect('usuario-criar-conta')
                return redirect('usuario-resumo')
            except:
                return redirect('usuario-criar-conta')
        else:
            return redirect('sistema-index')
    return decorator
