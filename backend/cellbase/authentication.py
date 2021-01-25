from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

"""
See: https://docs.djangoproject.com/en/3.0/topics/auth/default/#auth-web-requests
"""


@require_POST
def handle_login(request):
  print('login request')
  print(request)
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)

    # return HttpResponse('Successful login', status=200)
    data = {
      'message': 'Successful login',
      'first_name': user.first_name,
      'last_name': user.last_name,
    }
    return JsonResponse(data, status=200, safe=True)
  else:
    # Return an 'invalid login' error message.
    return HttpResponse('Unauthorized', status=401)


@require_POST
def handle_logout(request):
  logout(request)
  return HttpResponse('Successful logout', status=200)

