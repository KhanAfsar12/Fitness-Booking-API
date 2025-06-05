from django.db import models

# Create your models here.
class FitnessClass(models.Model):
    CLASS_CHOICES = [('Yoga', 'Yoga'), ('Zumba', 'Zumba'), ('HIIT', 'HIIT')]
    name = models.CharField(choices=CLASS_CHOICES, max_length=30)
    instructor = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} at {self.datetime}'
    

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class}"