from django.db import models
from django.contrib.auth.models import User


class WishItemManager(models.Manager):
    def unpurchased_for_user(self, user):
        return self.filter(purchased_by=None, wisher=user)

    def wanted_by_user(self, user):
        return self.filter(wisher=user)


class WishItem(models.Model):
    item_name = models.CharField(max_length=100)
    wisher = models.ForeignKey(User, related_name="wisher")
    purchased_by = models.ForeignKey(User, blank=True, null=True, related_name="buyer")

    objects = WishItemManager()

    def mark_purchased(self, buyer):
        self.purchased_by = buyer

    def __str__(self):
        return "{0} wished by {1}".format(self.item_name, self.wisher)
