from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

User = settings.AUTH_USER_MODEL


from .signals import object_viewed_signal
# Create your models here.

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL,
                                     null= True) #product, #post
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    viewed_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.content_object)

    class Meta:
        verbose_name_plural = 'Histories'


def object_viewed_receiver(sender, instance, request,
                           *args, **kwargs):
    new_history = History.objects.create(
        user            = request.user,
        content_type    = ContentType.objects.get_for_model(sender),
        object_id      = instance.id,

    )

object_viewed_signal.connect(object_viewed_receiver)