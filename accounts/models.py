from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
# ________________________________________________

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        
        if not email:
            raise ValueError(_("فیلد ایمیل نمیتوند خالی باشد"))
        
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("The is_active field for superuser must be enabled"))
        if extra_fields.get("is_admin") is not True:
            raise ValueError(_("The is_admin field for superuser must be enabled"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("The is_superuser field for superuser must be enabled"))
        
        return self.create_user(email,password, **extra_fields)
# ________________________________________________

class CustomUser(AbstractBaseUser,PermissionsMixin):
    """
    Custom User instead of User Django 
    """
    
    email = models.EmailField(max_length=128, verbose_name=_('ایمیل'),unique=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    update_date = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))
    is_active = models.BooleanField(default=False, verbose_name=_("فعال/غیرفعال"))
    is_admin = models.BooleanField(default=False, verbose_name=_("کاربر عادی / کاربر ادمین"))
    is_verficated = models.BooleanField(default=False, verbose_name=_("تاییدشده/تاییدنشده"))
    
    
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
# ________________________________________________

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=_("کاربر"), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    image_name = models.ImageField(upload_to='media/images/Profile/', null=True, blank=True, verbose_name=_("عکس پروفایل"))
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'
# ________________________________________________

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# ________________________________________________
