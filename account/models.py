from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import NullBooleanField
from django.template.defaultfilters import slugify

import uuid


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have a email address.')
        if not username:
            raise ValueError('Users must have a Username.')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
        )

        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    name                    = models.CharField(max_length=30, null=True, blank=True)
    bio                     = models.TextField(null=True, blank=True)
    profile_pic             = models.ImageField(default='default_pfp.jpg', upload_to="user_uploaded")
    website                 = models.URLField(max_length=300, null=True, blank=True)
    gender                  = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)

    date_joined             = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # Can Login with email address
    REQUIRED_FIELDS = ['username', ] # USERNAME_FIELD is required by default

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = 'default_pfp.jpg'
        return url


    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return True
    