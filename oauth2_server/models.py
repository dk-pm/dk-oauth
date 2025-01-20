from django.db import models

class DigikalaUser(models.Model):
    digikala_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    token = models.CharField(max_length=255)  # To store Digikala:User:Token:new
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" 