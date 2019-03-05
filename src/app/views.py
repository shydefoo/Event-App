from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.utils.custom_auth.jwt_auth_methods import validate_request


@validate_request()
def test_jwt_validation(request):
    return HttpResponse("token validation success")