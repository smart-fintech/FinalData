from django.db import models
# from OCR import imagepath
import os
from django.conf import settings
from e_checkapp.models import PpBnkM,PpOrgnM,User

# Create your models here.
class Post(models.Model):
    masterbankdata = models.ForeignKey(PpBnkM, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='images/')
    created_by=models.CharField(max_length=100)
    # output = models.FilePathField(path='inference/output/', match="*.csv", null=True, recursive=True)

    # def __str__(self):
    #     return self.masterbank_id


