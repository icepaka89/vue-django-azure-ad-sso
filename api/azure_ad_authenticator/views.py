from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from dateutil import tz, parser
from azure_ad_authenticator.auth.helpers.auth_helper import get_token_from_code, store_user, get_sign_in_flow, remove_user_and_token, get_token
from azure_ad_authenticator.auth.helpers.graph_helper import *
import logging

logger = logging.getLogger()

# Create your views here.
def index(request):
  return HttpResponse("Azure AD SSO Proof of Concept")

def sso_sign_in(request):
  # Get the sign-in flow
  flow = get_sign_in_flow()
  # Save the expected flow so we can use it in the callback
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
    print(e)
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(flow['auth_uri'])

def sso_callback(request):
  # Get the azure ad token info
  result = get_token_from_code(request)

  # Attempt to authenticate the user using the azure ad access token
  user = authenticate(request, token=result['access_token'])

  # If authentication succeeds, the user will have a value. Log them in and
  # redirect to dashboard
  if user is not None:
    login(request, user)
    return HttpResponseRedirect("http://localhost:8080/")
  # Otherwise, Redirect back to login page
  else:
    return HttpResponseRedirect("http://localhost:8080/")

def sign_out(request):
  remove_user_and_token(request)
  logout(request)

  return HttpResponseRedirect("http://localhost:8080/")

def sign_in(request):
  body = json.loads(request.body)
  user = authenticate(username=body['username'], password=body['password'])
  if user is not None:
    login(request, user)
    return HttpResponseRedirect("http://localhost:8080/")
  else:
    return HttpResponseRedirect("http://localhost:8080/")

def currentuser(request):
  if request.user and request.user.is_authenticated:
    return HttpResponse(request.user.username)
  else: 
    return HttpResponseForbidden('Not logged in!')