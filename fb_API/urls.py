from django.urls import path
from .views import *

urlpatterns = [
    path('classes/', FitnessClassList.as_view(), name='class-list'),
    path('book/', BookClass.as_view(), name='book-class'),
    path('bookings/', BookingList.as_view(), name='booking-list')
]