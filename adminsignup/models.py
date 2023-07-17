from django.db import models

# Create your models here.
class clubadmin(models.Model):
    CollegeName = models.CharField(max_length=200, null=True) 
    ClubName = models.CharField(max_length=120) 
    Email = models.CharField(max_length=120)
    phone = models.CharField(max_length=12,null=True)

    def __str__(self):
        return self.ClubName
     