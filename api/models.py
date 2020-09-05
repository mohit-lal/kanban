from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver 

# Create your models here.

class Organization(models.Model):
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="organization")
    image = models.ImageField(upload_to="organization", null=True, blank=True)
    address = models.CharField(max_length=500)
    location = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    mobile1 = models.CharField(max_length=20, null=True, blank=True)
    mobile2 = models.CharField(max_length=20, null=True, blank=True)
    email1 = models.EmailField()
    email2 = models.EmailField(null=True, blank=True)
    about = models.TextField()

    def __str__(self):
        return self.title


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        abstract = True

#Task Board model
class Board(models.Model):
    creator       = models.ForeignKey("members.Member", related_name="created_boards")
    name          = models.CharField(max_length=128)
    description   = models.TextField(max_length=128,default="", blank=True)
    comments      = models.TextField(max_length=128,default="", blank=True)
    uuid          = models.CharField(max_length=128, verbose_name=u"External id of the board", unique=True)
    last_activity_datetime = models.DateTimeField(verbose_name=u"Last activity date", default=None, null=True)
    is_archived = models.BooleanField(verbose_name=u"This board is archived",
                                      help_text=u"Archived boards are not fetched automatically and are ignored",
                                      default=False)
    enable_public_access = models.BooleanField(verbose_name=u"Enable public access to this board",
                                               help_text=u"Only when enabled the users will be able to access",
                                               default=False)
    public_access_code = models.CharField(max_length=32,
                                          verbose_name=u"External code of the board",
                                          help_text=u"With this code it is possible to access to a view with stats "
                                                    u"of this board", unique=True)
    last_fetch_datetime = models.DateTimeField(verbose_name=u"Last fetch datetime", default=None, null=True)
    members = models.ManyToManyField("members.Member", verbose_name=u"Members", related_name="boards")
    percentage_of_completion = models.DecimalField(
        verbose_name=u"Percentage of completion",
        help_text=u"Percentage of completion of project. Mind the percentage of completion of each requirement.",
        decimal_places=2, max_digits=10, blank=True, default=None, null=True
    )
    estimated_number_of_hours = models.PositiveIntegerField(verbose_name=u"Estimated number of hours to be completed",
                                                            help_text=u"Number of hours in the budget",
                                                            blank=True, default=None, null=True)
    hourly_rates = models.ManyToManyField("hourly_rates.HourlyRate", verbose_name=u"Hourly rates",
                                          related_name="boards", blank=True)
    header_image = models.ImageField(
        verbose_name=u"Header image", default=None, null=True, blank=True,
        help_text=u"Header image for this board. Optional."
    )
    identicon = models.ImageField(
        verbose_name=u"Identicon", default=None, null=True, blank=True,
        help_text=u"Identicon for this board. It is automatically generated and stored."
    )
    identicon_hash = models.CharField(max_length=256,
                                      verbose_name=u"Identicon hash",
                                      help_text=u"Identicon hash used to know when to update it",
                                      default="", blank=True)
    # Users that can view the board stats and other parameters but cannot change anything
    url = models.CharField(max_length=255, verbose_name=u"URL of the board", null=True, default=None)        