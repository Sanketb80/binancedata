from django.db import models

# Create your models here.
class symbolmaster(models.Model):
    symbol = models.CharField(max_length = 25,default = "NA")
    type = models.CharField(max_length = 25,default = "NA")
    ltp = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    onehr = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    onehrprice =models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    onehrchange = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    twohr = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    twohrprice = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    twohrchange = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    totalhr = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    totalhrprice = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    totalhrchange = models.DecimalField(max_digits = 13,decimal_places = 3,default = 0)
    
