from django.shortcuts import render

# Create your views here.
from auth_app.models import User


def ft(request):
    access_token = request.session.get('access_token')
    if access_token is None:
        return redirect('/')
    if access_token:
        try:
            user = User.objects.get(token_access=access_token)
        except User.DoesNotExist:
            return redirect('/')
    return render(request, 'chat/index.html', {'user': user})