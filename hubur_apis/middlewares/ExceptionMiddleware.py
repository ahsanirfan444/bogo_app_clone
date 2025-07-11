from rest_framework.views import exception_handler
from django.http import JsonResponse
from django.conf import settings
 
def get_response(message="", result={}, status=False, status_code=200):
   return {
       "detail" : message,
       "status" : status_code,
   }
 
def get_error_message(error_dict):
   response = error_dict[next(iter(error_dict))]
   if isinstance(response, dict):
       response = get_error_message(response)
   elif isinstance(response, list):
       response_message = response[0]
       if isinstance(response_message, dict):
           response = get_error_message(response_message)
       else:
           response = response[0]
   return response
 
def handle_exception(exc, context):
   error_response = exception_handler(exc, context)
   if error_response is not None:
       error = error_response.data
 
       if isinstance(error, list) and error:
           if isinstance(error[0], dict):
               error_response.data = get_response(
                   message=get_error_message(error),
                   status_code=error_response.status_code,
               )
 
           elif isinstance(error[0], str):
               error_response.data = get_response(
                   message=error[0],
                   status_code=error_response.status_code
               )
 
       if isinstance(error, dict):
           error_response.data = get_response(
               message=get_error_message(error),
               status_code=error_response.status_code
           )
   return error_response
 
class ExceptionMiddleware(object):
   def __init__(self, get_response):
       if not settings.DEBUG:
           self.get_response = get_response
 
   def __call__(self, request):
 
       response = self.get_response(request)
 
       if response.status_code == 500 and 'api/' in request.path:
           response = get_response(
               message="Internal server error! Email has been sent to the developer(s)",
               status_code=500
           )
           return JsonResponse(response, status=500)
 
       if response.status_code == 404 and 'api/' in request.path:
           response = get_response(
               message="Page not found, invalid url",
               status_code=404
           )
           return JsonResponse(response, status=404)
 
       return response