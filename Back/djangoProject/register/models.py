from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class Company(models.Model):
	companyName = models.CharField(max_length=100, null = True)
	officeNumber = models.IntegerField(null = True)
	iataCassNumber = models.IntegerField(null = True)
	address = models.CharField(max_length=100, null = True)
	city = models.CharField(max_length=100, null = True)
	state = models.CharField(max_length=100, null = True)
	zip = models.CharField(max_length=100, null = True)
	country = models.CharField(max_length=100, null = True)

	def __str__(self):
		return self.companyName
      
class RegistrationKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Check if the key is still within the 24-hour window and not used
        expiration_time = self.created_at + timezone.timedelta(hours=24)
        return not self.is_used and timezone.now() <= expiration_time

    def __str__(self):
        return str(self.key)
class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null =True)
