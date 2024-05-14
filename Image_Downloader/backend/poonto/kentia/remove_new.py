from PIL import Image
import io

# Atrocious legacy code I wrote 2 weeks into learning Python early in my career.
# Modified it to interface with my program.
# It crops away a [NEW] stamp from this supplier's product images.

def has_NEW(img) -> bool:
    row = 40
    column = 40
    try:  #checks for a specific magenta'ish color to determine if the "NEW" stamp exists.
        for i in range(10):
            for y in range(10):
                pixel = img.getpixel((row+y,column+i))
                if (225 <= pixel[0] and pixel[0] <= 232) and (2 <= pixel[1] and pixel[1] <= 10) and (120 <= pixel[2] and pixel[2] <= 130): 
                    return True
                else: break
    except: return False
    return False


def crop(img: Image.Image) -> None:
    cropbox = (0, 147, img.width, img.height) #left, upper, right, lower
    img = img.crop(cropbox)
 



def remove_new(image: Image.Image) -> None:
    if has_NEW(image):
        crop(image)
        


