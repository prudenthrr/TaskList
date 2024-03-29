from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.
class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)

class ListUserManager():

    def create_user(self,email):
        ListUser.objects.create(email=email)

    def create_superuser(self,email,password):
        self.create_user(email)


class ListUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email=='prudent_hrr@163.com'

    @property
    def is_active(self):
        return True

