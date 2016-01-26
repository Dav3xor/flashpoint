from django.shortcuts import render
from django.http import JsonResponse

from fpmessages.models import *
import sys

# decorator for automatically returning json with
# success/failure based on thrown exceptions.
#
# this would be a neat way to make a standardized
# REST api.
#
# Also, the results of the called function should
# probably be put under their own dictionary key,
# otherwise naming conflicts could occur.
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
  return { 'cities': Locations.fast_count(), 
           'users': Users.fast_count() }
