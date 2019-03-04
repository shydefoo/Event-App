from django.urls import path
from .api_endpoints import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get_events/', get_events)
]