
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    first_name = models.CharField(_("First Name"), null=False, max_length=20)
    last_name = models.CharField(_("Last Name"), null=False, max_length=20)
    email = models.EmailField(_("Email"), unique=True)
    profile_image = models.ImageField(upload_to='user_profile', default='user.jpg', null=False)
    slug = models.SlugField(editable=False, max_length=10, null=True)
    is_logged_in = models.BooleanField(default=False)

    def _generate_slug(self):

        random_value = str(random.randint(11111, 99999))
        value = f'{self.get_full_name()} {random_value}'
        slug_original = slugify(value, allow_unicode=True)

        if not User.objects.filter(slug=slug_original).exists():
            self.slug = slug_original

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_username()
