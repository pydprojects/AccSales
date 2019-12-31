from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile


def image_compressor(image, name):
    try:
        img = Image.open(image)
        img = img.resize((380, 480))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=80)
        # create a django-friendly Files object
        compressed_img = ImageFile(img_io, name=f'{name}.jpg')
        return compressed_img
    except IOError:
        print("Error during image converting.")
