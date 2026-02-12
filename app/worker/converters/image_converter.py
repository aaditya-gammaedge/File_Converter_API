from PIL import Image
from .base import BaseConverter


class JPGtoPNGConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        image = Image.open(input_path)
        image.save(output_path, "PNG")


class PNGtoJPGConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        image = Image.open(input_path).convert("RGB")
        image.save(output_path, "JPEG")
