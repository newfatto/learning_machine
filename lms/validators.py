from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


def youtube_link_validator(value):
    """
    Проверяет, что ссылка ведёт только на youtube.com или youtu.be.
    """

    parsed_url = urlparse(value)

    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValidationError("Некорректный URL.")

    allowed_domains = (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
    )

    if parsed_url.netloc not in allowed_domains:
        raise ValidationError("Разрешены только ссылки на YouTube.")

    return value
