import hashlib
import magic

from django.db.models import ImageField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ValidatedImageField(ImageField):
    """
    Extends Djangos ImageField by validating the uploaded file, setting the
    filename based on a hash of the file, and setting the extension based on
    the image type.
    """

    extensions = {
        'image/gif': '.gif',
        'image/jpeg': '.jpg',
        'image/png': '.png',
    }

    def name_image_by_contents(self, file):
        file.seek(0)
        m = magic.from_buffer(file.read(1024), mime=True)
        ext = self.extensions.get(m)
        if not ext:
            raise ValidationError(
                _('Unsupported image file format {}').format(m))
        file.seek(0)
        h = hashlib.sha224()
        h.update(file.read())
        return u'{}{}'.format(h.hexdigest(), ext)

    def __init__(self, *args, **kwargs):
        if 'extensions' in kwargs:
            self.extensions = kwargs.pop('extensions')
        super(ValidatedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ValidatedImageField, self).clean(*args, **kwargs)
        data.name = self.name_image_by_contents(data.file)
        return data


def show_toolbar_callback(request):
    """
    Custom callback to always show the debug toolbar when the DEBUG setting
    is True. See https://django-debug-toolbar.readthedocs.io/en/1.0/configuration.html#debug-toolbar-config
    """
    return settings.DEBUG
