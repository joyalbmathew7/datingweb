from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


class ImageCompressionService:

    MAX_WIDTH = 1600
    MAX_HEIGHT = 1600
    QUALITY = 85

    @staticmethod
    def compress_image(image):
        img = Image.open(image)

        # Convert images like PNG/RGBA to RGB
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize large images while keeping the aspect ratio
        img.thumbnail(
            (
                ImageCompressionService.MAX_WIDTH,
                ImageCompressionService.MAX_HEIGHT,
            ),
            Image.Resampling.LANCZOS,
        )

        output = BytesIO()

        img.save(
            output,
            format="JPEG",
            quality=ImageCompressionService.QUALITY,
            optimize=True,
        )

        output.seek(0)

        return ContentFile(
            output.read(),
            name=f"{image.name.rsplit('.', 1)[0]}.jpg",
        )