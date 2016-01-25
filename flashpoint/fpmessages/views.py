from django.shortcuts import render
from django.http import JsonResponse

from fpmessages.models import *
import sys

def return_json(fun):
  def wrapper(*args,**kwargs):
    try:
      output = fun(*args, **kwargs)
      output['result'] = "success"
      return JsonResponse(output)
    except Exception as e:
      output = {'result': 'error',
                'error':  e.message}
      return JsonResponse(output)
  return wrapper

@return_json
def stats(request):
  return { 'cities': Locations.count(), 
           'users': Users.count() }
