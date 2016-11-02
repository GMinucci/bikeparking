from django.shortcuts import redirect
from six import wraps
from parking.models import Person


def user_or_admin(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login-redirect')
        if not request.user.groups.filter(name='admin').exists():
            try:
                person = Person.objects.get(user=request.user)
                if person.cpf is "":
                    return redirect('usuario-criar-conta')
                return redirect('usuario-resumo')
            except:
                return redirect('usuario-criar-conta')
        else:
            return function(request, *args, **kwargs)
    return decorator


def admin_redirect_on_user(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login-redirect')
        if request.user.groups.filter(name='admin').exists():
            return redirect('login-redirect')
        return function(request, *args, **kwargs)
    return decorator
