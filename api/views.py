import operator
from datetime import datetime

# Django imports
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection

# Dependencies
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, SAFE_METHODS


from geopy.distance import geodesic

# Project
from .serializers import *
from .models import *
from recycling import utils

logger = utils.get_logger()


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

class RecyclableMaterialViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    model = RecyclableMaterial
    queryset = RecyclableMaterial.objects.all()
    serializer_class = RecyclableMaterialSerializer
    renderer_classes = (JSONRenderer, )

class RecyclableSpotViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    model = RecyclableSpot
    queryset = RecyclableSpot.objects.all()
    serializer_class = RecyclableSpotSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=False, methods=['get'])
    def nearby(self, request, pk=None):

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.all()


        # Calculate distance
        recyclable_spot_distance_list = {}
        for recyclable_spot in recyclable_spot_queryset:
            user_location = (user_latitude, user_longitude)
            spot_location = (recyclable_spot.latitude, recyclable_spot.longitude)
            recyclable_spot_distance_list[recyclable_spot.id] = geodesic(user_location, spot_location).kilometers

        # Get closest
        recyclable_spot_id_listed_sorted = sorted(recyclable_spot_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recyclable_spot_closest_id_list = [i[0] for i in recyclable_spot_id_listed_sorted[0:settings.RECYCLABLE_SPOTS_LIMIT]]
        recyclable_spot_closest_queryset = recyclable_spot_queryset.filter(pk__in=recyclable_spot_closest_id_list)

        # Generate serializer
        serializer = RecyclableSpotDistanceSerializer(recyclable_spot_closest_queryset,
                                                      context={'distance_list': recyclable_spot_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MaterialViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    renderer_classes = (JSONRenderer, )


class RankingView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request, format=None):

        with connection.cursor() as cursor:
            cursor.execute('Select auth_user.id as id, auth_user.username as username, count(api_recyclablehistory.created_at) as count ' +
                            'from auth_user ' +
                            'left join api_recyclablehistory ' +
                            'on auth_user.id = api_recyclablehistory.user_id ' +
                            'where auth_user.is_superuser=0 ' +
                            'group by auth_user.id ' +
                            'order by -count ')
            result = cursor.fetchall()

            # Generate User_List
            user_list = []
            #for user in result:
            for index, user in enumerate(result):
                user_list.append({'id': user[0], 'username': user[1], 'count': user[2], 'ranking': (index+1)})
            return Response(user_list,  status=status.HTTP_200_OK)

        # Return generic error
        return Response({'response': 'ko'},  status=status.HTTP_400_BAD_REQUEST)

class StatsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request, format=None):
        start_time = datetime.strptime(request.query_params.get('startdate'), '%Y-%m-%d')
        end_time = datetime.strptime(request.query_params.get('enddate'), '%Y-%m-%d')

        print("-- parsing time --")
        print(start_time)
        print(end_time)

        recyclable_history = RecyclableHistory.objects.filter(user=request.user)


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

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def recyclablespot(self, request, pk=None):

        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        # Retrieve object
        product = self.get_object()

        # M.aterial set
        material_set = product.material_set.all()

        # Get Recyclable Spot
        recyclable_spot_list = []
        for material in material_set:
            spot_queryset = RecyclableSpot.objects.filter(recyclable_material=material.recyclable_material)
            spot_list = list(spot_queryset.values_list('id', flat=True))
            recyclable_spot_list.extend(spot_list)

        # Get RecyclableSpot List
        recyclable_spot_queryset = RecyclableSpot.objects.filter(pk__in=recyclable_spot_list)

        # Calculate distance
        recyclable_spot_distance_list = {}
        for recyclable_spot in recyclable_spot_queryset:
            user_location = (user_latitude, user_longitude)
            spot_location = (recyclable_spot.latitude, recyclable_spot.longitude)
            recyclable_spot_distance_list[recyclable_spot.id] = geodesic(user_location, spot_location).kilometers

        # Get closest
        recyclable_spot_id_listed_sorted = sorted(recyclable_spot_distance_list.items(),
                                                    key=operator.itemgetter(1))
        recyclable_spot_closest_id_list = [i[0] for i in recyclable_spot_id_listed_sorted[0:settings.RECYCLABLE_SPOTS_LIMIT]]
        recyclable_spot_closest_queryset = recyclable_spot_queryset.filter(pk__in=recyclable_spot_closest_id_list)

        # Generate serializer
        serializer = RecyclableSpotDistanceSerializer(recyclable_spot_closest_queryset,
                                                      context={'distance_list': recyclable_spot_distance_list},
                                                      many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NewViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    model = New
    queryset = New.objects.all()
    serializer_class = NewSerializer
    renderer_classes = (JSONRenderer, )
