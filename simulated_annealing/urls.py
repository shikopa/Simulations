from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from simulated_annealing.salesman import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'city', views.CityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^cities/', views.city_list),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^anneal/$', views.city_list),
    url(r'^anneal/(?P<pk>[0-9]+)/$', views.city_detail),
]

# urlpatterns = format_suffix_patterns(urlpatterns)