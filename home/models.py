from django.db import models


# Create your models here.

class UserDetail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=15)

    def __str__(self):
         return self.name
    

class Quote(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    solar_kw_production = models.FloatField()
    battery_kw_production = models.FloatField()
    panel_pricing = models.FloatField()
    battery_pricing = models.FloatField()
    inverter_pricing = models.FloatField()
    panels_required_pdf = models.IntegerField()
    house_consumption_pdf = models.FloatField()
    battries_required_pdf = models.FloatField()
    required_inverter_pdf = models.IntegerField()
    total_cost = models.FloatField()

    def __str__(self):
        return f"Quote for {self.user.name}"