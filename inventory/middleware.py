from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                validated_token = self.jwt_authenticator.get_validated_token(token)
                request.user = self.jwt_authenticator.get_user(validated_token)
            except AuthenticationFailed:
                return JsonResponse({'detail': 'Invalid token'}, status=401)
        elif not request.path.startswith('/login/'):
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        return self.get_response(request)
