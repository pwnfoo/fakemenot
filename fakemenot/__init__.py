'''
This program uses pytesseract to do OCR on images.
Make sure you have the following packages installed on the system :

* tesseract
* tesseract-data-eng

Tested on Arch Linux - Rolling
'''

import argparse
import pytesseract
import configparser
from TwitterSearch import *
from PIL import Image, ImageEnhance, ImageFilter


'''Parses parameters for getting image input.
Please don't hate me for doing this right after import
(and for this ugly multiline comment)'''
parser = argparse.ArgumentParser(description='Process images')
parser.add_argument('--image', '-i', help='Twitter screenshot image', required=True)
parser.add_argument('--limit', '-l', help='Limit tweets pulled', default=100)

args = parser.parse_args()


def _do_ocr_and_lookup(img_obj):
    limit_of_tweets = int(args.limit)
    # Replace line breaks with a space and split text into an array
    text = pytesseract.image_to_string(img_obj, lang='eng').replace('\n', ' ').split(' ')
    for element in text:
        if element and element[0] == '@':
            # Since handles cannot have spaces, strip until space
            potential_user = element.split(' ')[0]
            break;

    config = configparser.RawConfigParser()
    config.readfp(open('twitter.config'))

    # Just in case, the dude/dudette using the program puts in ' or " in the config.
    consumer_key = config.get('twitter', 'consumer_key').replace('\'', '').replace('\"', '')
    consumer_secret = config.get('twitter', 'consumer_secret').replace('\'', '').replace('\"', '')
    access_token = config.get('twitter', 'access_token').replace('\'', '').replace('\"', '')
    access_token_secret = config.get('twitter', 'access_token_secret').replace('\'', '').replace('\"', '')

    try:
        tuo = TwitterUserOrder(potential_user[1:])
        ts = TwitterSearch(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = access_token,
            access_token_secret = access_token_secret
        )
        tweets = []
        for tweet in ts.search_tweets_iterable(tuo):
            # Nobody cares about re-tweets
            if 'RT ' not in tweet['text']:
                if tweet not in tweets:
                    tweets.append((tweet['text'], tweet['id']))
                if not limit_of_tweets:
                    break;
                else:
                    limit_of_tweets -= 1
        body = text[text.index('')+1:]
        try:
            stripped_body = body[:body.index('')]
        except:
            stripped_body = body

        for tweet in tweets:
            removed_elements = 0
            ltweet, orig_len = tweet[0].split(' '), len(tweet[0].split(' '))
            for ele in stripped_body:
                if ele in ltweet:
                    removed_elements += 1
                    ltweet.remove(ele)
            removal_rate = (removed_elements/float(orig_len))*100
            if removal_rate > 75.0 :
                print("*** Tweet is probably real! ***")
                print("-> Confidence : " + "%.2f"%removal_rate + "%")
                print("-> URL : https://twitter.com/"+potential_user[1:]+"/status/"+str(tweet[1]))


    except TwitterSearchException as e: # catch all those ugly errors
        print(e)


def _blow_up_image():
    try:
        img = Image.open(args.image)
    except FileNotFoundError:
        print("[!] I couldn't find a file by that name. Fake you!")
        return False

    basewidth = 2500
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


def main():
    img_obj = _blow_up_image()
    if img_obj:
        # Give that sexy image object to OCR to find potential user
        _do_ocr_and_lookup(img_obj)


if __name__ == '__main__':
    main()
