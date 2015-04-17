from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class UserAccountManager(BaseUserManager):
	# override create_user and create_superuser 
	def create_user(self, email,password=None, **kwargs):
		if not email:
			raise ValueError('Users must have a valid email address.')

		if not kwargs.get('username'):
			raise ValueError('Users must have a valid username.')

		account = self.model(
			email=self.normalize_email(email), username =kwargs.get('username')
		)
		account.set_password(password)
		account.save()
		
		return account

	def create_superuser(self,email,password=None,**kwargs):
		account = self.create_user(email,password,**kwargs)
		
		account.is_admin = True
		account.save()
		
		return account


class UserAccount(AbstractBaseUser):
	# use email as user name
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=40,unique=True)

	# firstname and last name are not mandatory	
	first_name = models.CharField(max_length=40,blank=True)
	last_name = models.CharField(max_length=40,blank=True)
	tagline = models.CharField(max_length=140,blank=True)

	is_admin = models.BooleanField(default=False)

	# created date to get updated automatically while adding
	created = models.DateField(auto_now_add=True)
	# modified date to get updated automatically while saving 
	modified = models.DateField(auto_now=True)
	
	objects = UserAccountManager()

	# becasue we are overriding AbstractBaseUser, we need to define below two fields
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	# tostring method
	def __unicode__(self):
		return self.email
	
	def get_full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def get_short_name(self):
		return self.first_name

