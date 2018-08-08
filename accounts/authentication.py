from accounts.models import User, Token


class PasswordlessAuthenticationBackend(object):
    ''' 无密码认证后端 '''

    def authenticate(self, uid):
        ''' 认证函数 '''
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
