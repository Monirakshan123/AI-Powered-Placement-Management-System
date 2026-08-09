from django.db import models
class AdminProfile(models.Model): 
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=100) 
    def str(self): 
        return self.name
