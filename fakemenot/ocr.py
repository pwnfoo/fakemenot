"""
This requires the tesseract library (with the english training data) to do OCR on images.
See https://github.com/tesseract-ocr/tesseract/wiki and https://pypi.python.org/pypi/pytesseract
for installation instructions.
"""

from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import image_to_string


def find_user_and_text_in_tweet_image(image_path):
    # OCR image
    image = prepare_image_for_ocr(image_path)
    if not image:
        return None, None

    # Split result into single words
    text = image_to_string(image, lang='eng')
    words = text.replace('\n', ' ').split(' ')

    # Delegate extraction of name and body to separate function.
    # Only the desktop detail view of a tweet is supported for now.
    return extract_values_from_desktop_tweet(words)


def extract_values_from_desktop_tweet(words):
    # Find user handle in words
    user = next((w for w in words if (w and len(w) > 1 and w[0] == '@')), None)

    # Find the tweet text body
    body = None
    if user:
        # Usually there are 2 random chars after the user handle, then the body starts.
        body_index = words.index(user) + 3

        if len(words) > body_index:
            body = " ".join(words[body_index:]).strip()

    return user, body


def prepare_image_for_ocr(image_path):
    # Open the image
    try:
        image = Image.open(image_path)
    except (OSError, IOError):
        return None

    # Resize image
    width = 4096.0
    height = width / image.size[0] * image.size[1]
    image = image.resize((int(width), int(height)), Image.ANTIALIAS)

    # Clean image and increase contrast. See: https://stackoverflow.com/a/37750605/5486120
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    return image
