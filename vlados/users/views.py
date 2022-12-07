import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignUpSerializer, UserSerializer


User = get_user_model()


class LoginRequiredViewSet(viewsets.ModelViewSet):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserViewSet(LoginRequiredViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        User.objects.get_or_create(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )
    except IntegrityError as error:
        error_text = f'{error}'
        if 'username' in error_text:
            message = 'Такой юзернейм уже занят'
        if 'email' in error_text:
            message = 'Такой email уже занят'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.validated_data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    """
    POST API for login
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": "User has been logged in"})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'You did logout'})
