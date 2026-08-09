from django.db import models


class InstitutionProfile(models.Model):

    institution_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=100
    )
    
    status = models.CharField( max_length=20, default='Pending' )

    address = models.TextField()


    def __str__(self):
        return self.institution_name