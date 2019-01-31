import operator
from datetime import datetime
from functools import wraps

# Django imports
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

# Dependencies
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import authentication
from rest_framework import exceptions

from geopy.distance import geodesic

# Project
from .serializers import *
from .models import *
from recycling import utils

logger = utils.get_logger()

# def view_or_retreive_user_id(view, request, *args, **kwargs):
#
#     # Check whether token is present
#     # Get URL Parameter
#     if request.GET.get('user_id') is not None:
#         model = get_user_model()
#         request.user = model.objects.get(id=request.GET.get('user_id'))
#
#     print("-- view_or_retreive_user_id --")
#     print(request.user)
#
#     return view(request, *args, **kwargs)
#
# def retrieve_user_id(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         return view_or_retreive_user_id(view_func, request, *args, **kwargs)
#     return wrapper
#
#
# class IsAdminUserOrReadOnly(IsAdminUser):
#
#     def has_permission(self, request, view):
#         is_admin = super(
#             IsAdminUserOrReadOnly,
#             self).has_permission(request, view)
#         # Python3: is_admin = super().has_permission(request, view)
#         return request.method in SAFE_METHODS or is_admin


class HeaderAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_USERNAME')
        if not username:
            return None

        try:
            user = get_user_model().objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


#@method_decorator(retrieve_user_id, name='dispatch')
class RecyclingAPIView(APIView):
    #pass
    #authentication_classes = (JWTAuthentication, HeaderAuthentication, )
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated,)

class RecyclingMaterialViewSet(viewsets.ModelViewSet, RecyclingAPIView):

    model = RecyclingMaterial
    queryset = RecyclingMaterial.objects.all()
    serializer_class = RecyclingMaterialSerializer
    renderer_classes = (JSONRenderer, )

class RecyclingPointViewSet(viewsets.ModelViewSet, RecyclingAPIView):

    model = RecyclingPoint
    queryset = RecyclingPoint.objects.all()
    serializer_class = RecyclingPointSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=False, methods=['get'])
    def nearby(self, request, pk=None):


        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        # Get RecyclingPoint List
        recycling_point_queryset = RecyclingPoint.objects.all()


        # Calculate distance
        recycling_point_distance_list = {}
        for recycling_point in recycling_point_queryset:
            user_location = (user_latitude, user_longitude)
            point_location = (recycling_point.latitude, recycling_point.longitude)
            recycling_point_distance_list[recycling_point.id] = geodesic(user_location, point_location).kilometers

        # Get closest
        recycling_point_id_listed_sorted = sorted(recycling_point_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recycling_point_closest_id_list = [i[0] for i in recycling_point_id_listed_sorted[0:settings.RECYCLING_POINT_LIMIT]]
        recycling_point_closest_queryset = recycling_point_queryset.filter(pk__in=recycling_point_closest_id_list)

        # Generate serializer
        serializer = RecyclingPointDistanceSerializer(recycling_point_closest_queryset,
                                                      context={'distance_list': recycling_point_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MaterialViewSet(viewsets.ModelViewSet, RecyclingAPIView):

    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    renderer_classes = (JSONRenderer, )


class RankingView(RecyclingAPIView):

    def get(self, request, format=None):

        with connection.cursor() as cursor:
            cursor.execute('Select auth_user.id as id, auth_user.username as username, count(api_recyclinghistory.created_at) as count ' +
                            'from auth_user ' +
                            'left join api_recyclinghistory ' +
                            'on auth_user.id = api_recyclinghistory.user_id ' +
                            'where auth_user.is_superuser=0 ' +
                            'group by auth_user.id ' +
                            'order by -count ')
            result = cursor.fetchall()

            # Generate User_List
            user_list = []
            for index, user in enumerate(result):
                user_list.append({'id': user[0], 'username': user[1], 'count': user[2], 'ranking': (index+1)})
            return Response(user_list,  status=status.HTTP_200_OK)

        # Return generic error
        return Response({'response': 'ko'},  status=status.HTTP_400_BAD_REQUEST)

class StatsView(RecyclingAPIView):

    def get(self, request, format=None):

        start_time = datetime.strptime(request.query_params.get('startdate'), '%Y-%m-%d')
        end_time = datetime.strptime(request.query_params.get('enddate'), '%Y-%m-%d')

        recycling_history = RecyclingHistory.objects.filter(user=request.user)

        response = {
            'n_scan': 876,
            'ranking': 765,
            'green_impact': 81.8,
            'weekly': {
                'n_scan': 103,
                'material_set' : {
                    'cardboard': 50,
                    'paper': 30,
                    'aluminum':20
                }
            },
            'monthly': {
                'n_scan': 221,
                'material_set' : {
                    'cardboard': 50,
                    'paper': 30,
                    'aluminum':20
                }
            },
            'yearly': {
                'n_scan': 456,
                'material_set' : {
                    'cardboard': 50,
                    'paper': 30,
                    'aluminum':20
                }
            }
        }

        # Return generic response
        return Response(response, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet, RecyclingAPIView):

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def recyclingpoint(self, request, pk=None):
        print(request.user)

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        # Retrieve object
        product = self.get_object()

        # M.aterial set
        material_set = product.material_set.all()

        # Get Recycling Point
        recycling_point_list = []
        for material in material_set:
            point_queryset = RecyclingPoint.objects.filter(recycling_material=material.recycling_material)
            point_list = list(point_queryset.values_list('id', flat=True))
            recycling_point_list.extend(point_list)

        # Get RecyclingPoint List
        recycling_point_queryset = RecyclingPoint.objects.filter(pk__in=recycling_point_list)

        # Calculate distance
        recycling_point_distance_list = {}
        for recycling_point in recycling_point_queryset:
            user_location = (user_latitude, user_longitude)
            point_location = (recycling_point.latitude, recycling_point.longitude)
            recycling_point_distance_list[recycling_point.id] = geodesic(user_location, point_location).kilometers

        # Get closest
        recycling_point_id_listed_sorted = sorted(recycling_point_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recycling_point_closest_id_list = [i[0] for i in recycling_point_id_listed_sorted[0:settings.RECYCLING_POINT_LIMIT]]
        recycling_point_closest_queryset = recycling_point_queryset.filter(pk__in=recycling_point_closest_id_list)

        # Generate serializer
        serializer = RecyclingPointDistanceSerializer(recycling_point_closest_queryset,
                                                      context={'distance_list': recycling_point_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewViewSet(viewsets.ModelViewSet, RecyclingAPIView):

    model = New
    queryset = New.objects.all()
    serializer_class = NewSerializer
    renderer_classes = (JSONRenderer, )
