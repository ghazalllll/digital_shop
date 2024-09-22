import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, send_mail,BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True


    def _create_user(self,username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email= self.normalise_email(email)
        user=self.model(phone_number=phone_number,username=username,email=email,
                        is_staff=is_staff,is_active=True,is_superuser=is_superuser,
                        date_joined=now,**extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,username=None,phone_number=None,email=None,password=None,**extra_fields):
        if username is None:
            if email:
                username=email.split('@',1)[0]
            if phone_number:
                username=random.choice('abcdefghijklmnopqrstuvwxyz')+str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username+=str(random.randint(10,99))        

        return self._create_user(username,phone_number,email,password,False,False,**extra_fields) 
    
    def create_superuser(self,username,phone_number,email,password,**extra_fields):
        return self._create_user(username,phone_number,email,password,True,True,**extra_fields) 
    def get_by_phone_number(self,phone_number):
        return self.get(**{'phone_number':phone_number})



class User(AbstractBaseUser, PermissionsMixin):
     username=models.CharField(_('username'),max_length=32,unique=True,
                               help_text=_('Use 30 characters or less that include letters and numbers'),
                               validators=[validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                                     _("Enter a valid username starting with a-z and containing letters, numbers, underscores, or periods."),
                                                                     'invalid' )],
                                error_messages={'unique':_("Duplicate username"),})
     first_name = models.CharField(_('first name'),max_length=30,blank=True)
     last_name =  models.CharField(_('last name'),max_length=30,blank=True)
     email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
     phone_number = models.BigIntegerField(_('mobile number'),unique=True, null=True, blank=True,
                               validators=[
                                   validators.RegexValidator(r'^989[0-3,9]\d{8$}',
                                                             ('Enter valid number'))],
                                error_messages={'unique':_("Duplicate mobile number")})
     is_staff = models.BooleanField(_('staff status'), default=False,
                                    help_text=_('designates whether the user can log into this admin site')) 
     is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('designates whether the user should be treated as active ,unselect this instead of deleting accounts.'))
     date_joined = models.DateTimeField(_('time joined'),default=timezone.now)
     last_seen = models.DateTimeField(_('last seen date'), null=True)


     objects = UserManager()
     USERNAME_FIELD = 'email'            
     REQUIRED_FIELDS = ['username', 'phone_number']

     class Meta:
        db_table = 'users'
        verbose_name= _('user')
        verbose_name_plural = _('users')

     def get_full_name(self):
        full_name='%s %s' % (self.first_name,self.last_name)
        return full_name.strip()

     def get_short_name(self):
        return self.first_name

     def email_user(self,subject,message,from_email=None,**kwargs):

        send_mail(subject, message, from_email,[self.email],**kwargs)     

     @property
     def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None

     def save(self,*args,**kwargs):
        if self.email is not None and self.email.strip() =='':
            self.email=None
        super().save(*args,**kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'),max_length=150,blank=True)
    avatar = models.ImageField(_('avatar'),blank=True)
    birthday = models.DateField(_('birthday'),null=True,blank=True)
    gender = models.BooleanField(_('gender'), null=True, help_text=_('female is False, male is True, null is unset'))
    province = models.ForeignKey(verbose_name=_('province'),to='Province',null=True,on_delete=models.SET_NULL)

class Province(models.Model):
    name = models.CharField(_('province name'), max_length=100)

    class Meta:
        verbose_name = _('province')
        verbose_name_plural = _('provinces')

    def __str__(self):
        return self.name