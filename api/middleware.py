from recycling import utils
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.http import Http404, HttpResponse
import json

logger = utils.get_logger()

class UserRetrieveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Get URL Parameter
        if request.GET.get('user_id') is None:
            return HttpResponse(json.dumps({'error': 'you did not provide user_id'}),
                                status=404,
                                content_type="application/json")

        model = get_user_model()
        request.user = model.objects.get(id=request.GET.get('user_id'))

        # Call View
        response = self.get_response(request)


        # Code to be executed for each request/response after
        # the view is called.

        return response
