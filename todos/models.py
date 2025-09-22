from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# ________________________________________________


class Todo(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('عنوان تسک'))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_('تاریخ ایجاد')
    )
    update_date = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))
    published_date = models.DateTimeField(
        default=datetime.now, verbose_name=_('تاریخ انتشار')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))
    is_done = models.BooleanField(default=False, verbose_name=_('انجام شده'))
    author = models.ForeignKey(
        "accounts.CustomUser",
        verbose_name=_("نویسنده"),
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تسک'
        verbose_name_plural = 'تسک ها'


# ________________________________________________
