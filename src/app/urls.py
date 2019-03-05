from django.urls import path
from .api_endpoints import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get_events/', get_events),
    path('get_photos_by_event/<uuid:event_id>', get_event_photos),
    path('get_event_comments/<uuid:event_id>', get_event_comments),
    path('join_event/', join_event),
    path('like_event/', like_event),
    path('comment_event/', comment_on_event)
]