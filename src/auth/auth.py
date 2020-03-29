import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'ffee.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = "https://nyah.com"
## AuthError Exception
class AuthError(Exception):
    def __init__(self, error_dict, code):
        self.error = error_dict['error']
        self.description = error_dict['description']
        self.status_code = code


def get_token():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'error': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'error': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'error': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'error': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def get_payload(token):
   """Obtains the payload from the jwt token
   """
   jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
   jwks = json.loads(jsonurl.read())
   unverified_header = jwt.get_unverified_header(token)
   rsa_key = {}
   if 'kid' not in unverified_header:
      raise AuthError({
         'error': 'invalid_header',
         'description': 'Authorization malformed.'
      }, 401)

   for key in jwks['keys']:
      if key['kid'] == unverified_header['kid']:
         rsa_key = {
             'kty': key['kty'],
             'kid': key['kid'],
             'use': key['use'],
             'n': key['n'],
             'e': key['e']
         }
   if rsa_key:
      try:
         payload = jwt.decode(
             token,
             rsa_key,
             algorithms=ALGORITHMS,
             audience=API_AUDIENCE,
             issuer='https://' + AUTH0_DOMAIN + '/'
         )
         print('payload:!!!!!{}'.format(payload))
         return payload

      except jwt.ExpiredSignatureError:
         raise AuthError({
             'error': 'token_expired',
             'description': 'Token expired.'
         }, 401)

      except jwt.JWTClaimsError:
         raise AuthError({
             'error': 'invalid_claims',
             'description': 'Incorrect claims. Please, check the audience and issuer.'
         }, 401)
      except Exception:
         raise AuthError({
             'error': 'invalid_header',
             'description': 'Unable to parse authentication token.'
         }, 400)
      raise AuthError({
             'error': 'invalid_header',
             'description': 'Unable to find the appropriate key.'
         }, 401)


def check_permissions(permission, payload):
   """check the permission with api permission and the permission in the payload of jwt
   """
   if 'permissions' not in payload:
      raise AuthError({
          'error': 'invalid_claims',
          'description': 'Permissions not included in JWT.'
      }, 400)

   if permission not in payload['permissions']:
      raise AuthError({
         'error': 'unauthorized',
         'description': 'Permission not found.'
      }, 403)
   return True


def requires_auth(permission=''):
   """api auth decorator
   """
   def requires_auth_decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
         token = get_token()
         payload = get_payload(token)

         check_permissions(permission, payload)
         return f(payload, *args, **kwargs)

      return wrapper
   return requires_auth_decorator