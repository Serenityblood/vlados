from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import login_view, logout_view, signup, UserViewSet

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('v1/', include(router_v1.urls))
]
