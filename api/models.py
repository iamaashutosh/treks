from django.db import models

# Create your models here.
class Trail(models.Model):

    name = models.CharField(max_length=50,null=True,blank=True)
    description=models.CharField(max_length=50,null=True,blank=True)
    #image=models.ImageField(null=True,blank=True)
    region=models.CharField(max_length=50,null=True,blank=True)
    distance_km=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    duration_days=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    elevation=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    difficulty=models.CharField(max_length=50,null=True,blank=True)
    start_lat = models.FloatField()
    start_lng = models.FloatField()
    end_lat = models.FloatField()
    end_lng = models.FloatField()

    def __str__(self):
        return self.name
class TrailImage(models.Model):
    trail = models.ForeignKey(Trail,related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.trail.name
class Test(models.Model):
    name =  models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)