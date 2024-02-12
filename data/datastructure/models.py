from django.db import models

# Create your models here.
class symbolmaster(models.Model):
    symbol = models.CharField(max_length = 25,default = "NA")
    type = models.CharField(max_length = 25,default = "NA")
    ltp = models.CharField(max_length = 25,default = "NA")
    onehr = models.CharField(max_length = 25,default = "NA")
    onehrprice =models.CharField(max_length = 25,default = "NA")
    onehrchange = models.CharField(max_length = 25,default = "NA")
    twohr = models.CharField(max_length = 25,default = "NA")
    twohrprice = models.CharField(max_length = 25,default = "NA")
    twohrchange = models.CharField(max_length = 25,default = "NA")
    totalhr = models.CharField(max_length = 25,default = "NA")
    totalhrprice = models.CharField(max_length = 25,default = "NA")
    totalhrchange = models.CharField(max_length = 25,default = "NA")

    