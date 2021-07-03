from .views import AmbassadorAPIView
from django.urls import path, include

urlpatterns = [
    path('', include('common.urls')),
    path('ambassadors', AmbassadorAPIView.as_view()),

]
