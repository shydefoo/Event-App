from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.api_endpoints import redirect_func
from app.utils.custom_auth.jwt_auth_methods import validate_request


@validate_request(redirect_func)
def test_jwt_validation(request):
    return HttpResponse("token validation success")