from rest_framework import routers
from .views import ApiAlbumsViewSet

app_name = 'account'

albums_router = routers.DefaultRouter()
albums_router.register(r'albums', ApiAlbumsViewSet, basename='albums')

urlpatterns = [
] + albums_router.urls
