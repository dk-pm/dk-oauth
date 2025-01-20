import requests
from django.conf import settings
from .models import DigikalaUser

class DigikalaAuthBackend:
    def authenticate(self, request, digikala_token=None):
        if not digikala_token:
            return None
            
        headers = {
            'Cookie': f'Digikala:User:Token:new={digikala_token}'
        }
        
        response = requests.get(
            'https://api.digikala.com/user/init/',
            headers=headers
        )
        
        data = response.json()
        if not data['data']['is_logged_in']:
            return None
            
        user_data = data['data']['user']
        
        user, created = DigikalaUser.objects.get_or_create(
            digikala_id=user_data['id'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'mobile': user_data['mobile'],
                'token': digikala_token
            }
        )
        
        if not created:
            user.token = digikala_token
            user.save()
            
        return user

    def get_user(self, user_id):
        try:
            return DigikalaUser.objects.get(pk=user_id)
        except DigikalaUser.DoesNotExist:
            return None 