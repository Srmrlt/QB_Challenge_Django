from django.urls import path
from .views import IsinExistsView, IsinExistsIntervalView, IidToIsinView

urlpatterns = [
    path('isin_exists', IsinExistsView.as_view(), name='isin_exists'),
    path('isin_exists_interval', IsinExistsIntervalView.as_view(), name='isin_exists_interval'),
    path('iid_to_isin', IidToIsinView.as_view(), name='iid_to_isin'),
]
