from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)



# class Weapon(models.Model):
#     power = models.IntegerField()
#     rarity = models.CharField(max_length=50)
#     value = models.IntegerField()
    

# one
class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


# to many
class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now=True)

