from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from advertise.validators import ImageCountValidator

User = get_user_model()


class Advertise(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ads'
    )
    title = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return f"{self.title} {self.price}"


class AdvertiseImage(models.Model):
    advertise = models.ForeignKey(
        Advertise, on_delete=models.CASCADE, related_name='images',
        validators=[ImageCountValidator(Advertise, 3)]
    )
    image = models.ImageField(upload_to='advertise_images/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ])
