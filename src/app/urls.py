from django.urls import path

from app.views import test_jwt_validation
from .api_endpoints import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get_jwt_token/', get_jwt_token),
    path('get_events/', get_events),
    path('get_photos_by_event/<uuid:event_id>', get_event_photos),
    path('get_event_comments/<uuid:event_id>', get_event_comments),
    path('get_event_participants/<uuid:event_id>', get_event_participants),
    path('get_event_likes/<uuid:event_id>', get_event_likes),
    path('join_event/', join_event),
    path('leave_event/', leave_event),
    path('like_event/', like_event),
    path('dislike_event/', dislike_event),
    path('comment_event/', comment_on_event),
    path('search_event/', search_events)
]

urlpatterns += [
    path('auth/testing/', test_jwt_validation)
]