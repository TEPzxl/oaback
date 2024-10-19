import jwt
from django.conf import settings
from jwt import ExpiredSignatureError
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from apps.oaauth.models import OAUser


def generate_jwt(user):
    expire_time = 60 * 60 * 24 * 7
    return jwt.encode({'userid': str(user.pk), 'exp': expire_time}, key=settings.SECRET_KEY, algorithm='HS256')


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = 'JWT'
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 2:
            msg = '不可用的请求头'
            raise AuthenticationFailed(msg)

        try:
            jwt_token = auth[1].decode()
            jwt_info = jwt.decode(jwt_token, key=settings.SECRET_KEY, algorithms=['HS256'])
            userid = jwt_info.get('userid')
            try:
                user = OAUser.objects.get(pk=userid)
                request.user = user
                return user, jwt_token
            except OAUser.DoesNotExist:
                raise exceptions.AuthenticationFailed('用户不存在')
        except ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('JWT Token已过期')

