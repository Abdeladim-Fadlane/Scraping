from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from urllib.parse import urlencode
import requests # type: ignore
from .models import User
import secrets
import os


state = secrets.token_urlsafe(16)
client_id =  os.environ.get('client_id')
redirect_uri = os.environ.get('redirect_uri')
client_secret = os.environ.get('client_secret')


def redirect_to_42(request):
    data = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'public',
        'state': state
    }
    authorize_url = f"https://api.intra.42.fr/oauth/authorize?{urlencode(data)}"
    return redirect(authorize_url)


def exchange_code_for_token(code):
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url,data=data)
    response_data = response.json()
    if 'access_token' in response_data :
        access_token = response_data['access_token']
        return access_token
    else:
        return None
    

def store_data_in_database(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        id = user_data['id']
        if not User.objects.filter(user_id=id):
            User.objects.create(
                user_id=user_data['id'],
                token_access=access_token,
                email=user_data['email'],
                login=user_data['login'],
                display_name=user_data['displayname'],
                image_url=user_data['image']['versions']['large']
            )
        else:
            User.objects.filter(user_id=id).update(
                token_access=access_token,
            )

def callback(request):
    code = request.GET.get('code')
    state_req = request.GET.get('state')
    if state_req != state :
        return HttpResponseBadRequest("invalid state parameter")
    access_token = exchange_code_for_token(code)

    if access_token :
        request.session['access_token'] = access_token
        store_data_in_database(access_token)
        return redirect('/game')    
    else:
        return HttpResponseBadRequest("Failed to authenticate")
    

