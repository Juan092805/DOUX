from django.urls import path
from .views import stats

urlpatterns = [
    path("dashboard/stats/", stats, name="admin_stats"),
]
