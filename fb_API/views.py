from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

from .serializers import BookingSerializer, FitnessClassSerializer

from .models import Booking, FitnessClass

# Create your views here.
class FitnessClassList(APIView):
    def get(self, request):
        classes = FitnessClass.objects.all()
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)
    

class BookClass(APIView):
    def post(self, request):
        data = request.data
        fitness_names = FitnessClass.objects.values_list('name', flat=True).distinct()

        try:
            if not FitnessClass.objects.filter(name__iexact=data.get('class_name')):
                return JsonResponse({'message': f'Entered class name is invalid ! Please enter one {list(fitness_names)}'}, status=400)
            fitness_class = FitnessClass.objects.get(name__iexact=data.get('class_name'))
            if fitness_class.available_slots <= 0:
                return JsonResponse({'message': f'No slots avalible, try after some times or choose another {list(fitness_names)}'}, status=400)
            if any([
                not data.get('client_name') or not str(data.get('client_name')).strip(),
                not data.get('client_email') or not str(data.get('client_email')).strip()
            ]):
                return JsonResponse({"message": 'All fields are required, Please check missing fields'}, status=400)
            Booking.objects.create(fitness_class=fitness_class, client_name=data['client_name'], client_email=data['client_email'])
            fitness_class.available_slots -= 1
            fitness_class.save()

            return JsonResponse({'message': 'Booking Successful'})
        except KeyError:
            return JsonResponse({'message': 'Missing Required fields'}, status=400)
        except FitnessClass.DoesNotExist:
            return JsonResponse({'message': 'Class not found'}, 404)
        


class BookingList(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email or not str(email).strip():
            return JsonResponse({'message': 'Email is required'}, status=400)
        bookings = Booking.objects.filter(client_email=email)
        serializers = BookingSerializer(bookings, many=True)
        return Response(serializers.data)