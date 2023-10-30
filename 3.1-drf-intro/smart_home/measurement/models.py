from django.db import models
  

# one
class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


# to many
class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='measurement_images/', blank=True, null=True)

