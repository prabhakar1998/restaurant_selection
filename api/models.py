import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api.utils import UserTypes


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        primary_key=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("This username is already used by another user."),
        },
    )
    user_type = models.IntegerField(
        verbose_name=_("User Type"),
        default=UserTypes.EMPLOYEE,
        choices=UserTypes.choices(),
    )

    def __str__(self):
        return self.username


class Employee(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    department = models.CharField(
        verbose_name=_("Department Name"),
        max_length=150,
        default="",
    )
    date_joined = models.DateTimeField(default=timezone.now, blank=True, editable=False)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]


class Restaurant(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="restaurant_profile",
    )
    restaurant_name = models.CharField(
        verbose_name=_("Restaurant Name"), max_length=150
    )

    def __str__(self):
        return self.restaurant_name

    class Meta:
        ordering = ["restaurant_name"]


class Menu(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(_("Menu Title"), max_length=250)

    description = models.CharField(_("Menu Description"), max_length=500, default=None)

    date_posted = models.DateField(
        default=datetime.date.today,
        db_index=True,
        editable=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date_posted", "restaurant"]


class Vote(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restaurant",
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="employee",
    )

    date_voted = models.DateField(
        default=datetime.date.today,
        db_index=True,
        editable=False,
    )

    class Meta:
        ordering = ["-date_voted"]
