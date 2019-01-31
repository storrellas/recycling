# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Project imports
from .views import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['name'] = 'Sergi'

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

router = routers.DefaultRouter()
router.register(r'recyclingmaterial', RecyclingMaterialViewSet)
router.register(r'recyclingpoint', RecyclingPointViewSet)
router.register(r'material', MaterialViewSet)
router.register(r'product', ProductViewSet)
router.register(r'new', NewViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/$', TokenObtainPairView.as_view(), name='api-token'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='api-token-refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='api-token-refresh'),
    url(r'^ranking/$', RankingView.as_view(), name='ranking'),
    url(r'^stats/$', StatsView.as_view(), name='stats'),
    url(r'^location/default/$', DefaultLocationView.as_view(), name='default-location'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
