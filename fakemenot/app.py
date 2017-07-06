import argparse
import pytesseract
import ConfigParser
from PIL import Image, ImageEnhance, ImageFilter

parser = argparse.ArgumentParser(description='Process images')
parser.add_argument('--image', '-i', help='Twitter screenshot image', required=True)
args = parser.parse_args()




def _blow_up_image():
    try:
        img = Image.open(args.image)
    except FileNotFoundError:
        print("[!] I couldn't find a file by that name. Fake you!")
        return False

    basewidth = 1500
    img = Image.open(args.image)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    # Resize happens here
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)

    # Thanks Stack Overflow <3 : https://stackoverflow.com/a/37750605/5486120
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    # Return the sexy image object
    return img


if __name__ == '__main__':

    img_obj = _blow_up_image()
    # Give that sexy image object to OCR to find potential user
