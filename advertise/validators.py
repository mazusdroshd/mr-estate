from django.core.exceptions import ValidationError
from django.db import models


class ImageCountValidator:
    def __init__(self, model: models.Model, max_count: int = 3):
        self._model = model
        self._max_count = max_count

    def __call__(self, value: int):
        obj = self._model.objects.get(id=value)
        if obj.images.count() >= 3:
            raise ValidationError('this ad has maximum number of images (3).')

    def __eq__(self, other):
        return (
            isinstance(other, ImageCountValidator)
            and self._model == other._model
            and self._max_count == other._max_count
        )

    def deconstruct(self):
        path = 'advertise.validators.ImageCountValidator'
        kwargs = {'model': self._model, 'max_count': self._max_count}
        return (path, (), kwargs)
