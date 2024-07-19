from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from .models import ContestantImage


@receiver(post_save, sender=ContestantImage)
def resize_contestant_image(sender, instance, created, **kwargs):
    if created:
        if instance.image:
            # Open the uploaded image using Pillow
            img = Image.open(instance.image.path)
            # Resize the image to 423x432
            resized_img = img.resize((1024, 1024))
            # Save the resized image back to the same location
            resized_img.save(instance.image.path)
