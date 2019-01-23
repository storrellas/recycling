# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Project imports
from .views import *

router = routers.DefaultRouter()
router.register(r'recyclablematerial', RecyclableMaterialViewSet)
router.register(r'recyclablespot', RecyclableSpotViewSet)
router.register(r'material', MaterialViewSet)
router.register(r'product', ProductViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/$', TokenObtainPairView.as_view(), name='api-token'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='api-token-refresh'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
