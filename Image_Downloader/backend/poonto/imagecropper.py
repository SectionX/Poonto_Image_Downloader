from PIL import Image
import io

def resize_image(imagebytes: bytes, dimensions: tuple[int, int], extension: str) -> bytes:
        background = Image.new(mode='RGB', size=(740, 740), color=(255,255,255))
        new_image = Image.open(io.BytesIO(imagebytes))
        new_image.thumbnail(dimensions)
        correction_width = (dimensions[0] - new_image.width) // 2
        correction_height = (dimensions[1] - new_image.height) // 2
        background.paste(new_image, box=(correction_width, correction_height))

        if extension == 'jpg': extension = 'jpeg'

        with io.BytesIO() as buffer:
            background.save(buffer, extension)
            buffer.seek(0)
            return buffer.read()


















