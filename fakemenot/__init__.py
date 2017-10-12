'''
This program uses pytesseract to do OCR on images.
Make sure you have the following packages installed on the system :

* tesseract
* tesseract-data-eng

Tested on Arch Linux - Rolling
'''

import argparse
import os
import sys
import pytesseract
import configparser
from TwitterSearch import *
from PIL import Image, ImageEnhance, ImageFilter
from termcolor import colored


parser = argparse.ArgumentParser(description='Process images')
parser.add_argument(
    '--image',
    '-i',
    help='Twitter screenshot image',
    required=True)
parser.add_argument('--limit', '-l', help='Limit tweets pulled', default=250)
parser.add_argument(
    '--config',
    '-c',
    help='Path to twitter config (default: ~/.fakemenot.config)',
    default="~/.fakemenot.config")

args = parser.parse_args()


def get_config():
    config = configparser.RawConfigParser()
    try:
        with open(os.path.expanduser(args.config)) as config_file:
            config.readfp(config_file)
    except IOError as ioe:
        print(colored("Couldn't open the config file {} because {}".format(
            args.config, ioe), 'red'))
        sys.exit(2)
    return config


def _do_ocr_and_lookup(img_obj):
    config = get_config()
    limit_of_tweets = int(args.limit)
    potential_user = '__fakemenot__'
    # Replace line breaks with a space and split text into an array
    text = pytesseract.image_to_string(
        img_obj, lang='eng').replace(
        '\n', ' ').split(' ')
    for element in text:
        if element and element[0] == '@':
            print("Detected handle : " + str(element))
            # Since handles cannot have spaces, strip until space
            potential_user = element.split(' ')[0]
            break

    # Just in case the person Yousing the program puts in ' or " in the config.
    consumer_key = config.get(
        'twitter',
        'consumer_key').replace(
            '\'','').replace(
                '\"','')
    consumer_secret = config.get(
        'twitter',
        'consumer_secret').replace(
            '\'','').replace(
                '\"','')
    access_token = config.get(
        'twitter',
        'access_token').replace(
            '\'','').replace(
                '\"','')
    access_token_secret = config.get(
        'twitter',
        'access_token_secret').replace(
            '\'','').replace(
                '\"','')

    if potential_user == '__fakemenot__':
        print(colored("[*] It looks like OCR failed. Please make sure you " +
            "crop the image as in sample and is readable.", 'red'))
        exit(1)

    try:
        tuo = TwitterUserOrder(potential_user[1:])
        ts = TwitterSearch(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        tweets = []
        body = '__awesomebody__'
        for tweet in ts.search_tweets_iterable(tuo):
            # Nobody cares about re-tweets
            if 'RT ' not in tweet['text']:
                if tweet not in tweets:
                    tweets.append((tweet['text'], tweet['id']))
                if not limit_of_tweets:
                    break
                else:
                    limit_of_tweets -= 1

        # The most probable tweet body is this.
        try:
            body = text[text.index('V') + 1:]
        except BaseException:
            body = text[text.index('v') + 1:]

        # If none of that was found, let's report an OCR error
        if body == '__awesomebody__':
            print(colored("[*] It looks like OCR failed.Please make sure you " +
                          "crop image as in sample and is readable.", 'red'))

        found_tweet = False
        # Check against every tweet pulled
        for tweet in tweets:
            removed_elements = 0
            ltweet, orig_len = tweet[0].split(' '), len(tweet[0].split(' '))
            # Compare each element of body to element in body. TODO: Optimize
            for ele in body:
                if ele in ltweet:
                    removed_elements += 1
                    ltweet.remove(ele)
            removal_rate = (removed_elements / float(orig_len)) * 100

            if int(removal_rate) in range(75, 100):
                found_tweet = True
                print(colored("[*] It looks like this is a valid tweet",
                              'green'))
                print(colored("-> Confidence : " + "%.2f" % removal_rate + "%",
                              'green'))
                print(colored("-> Potential URL : https://twitter.com/" +
                              potential_user[1:] +
                              "/status/" + str(tweet[1]), 'green'))

            elif int(removal_rate) in (55, 75):
                found_tweet = True
                print(colored("[*] This might be a valid tweet", 'yellow'))
                print(colored("-> Confidence : " + "%.2f" % removal_rate + "%",
                              'yellow'))
                print(colored("-> Potential URL : https://twitter.com/" +
                              potential_user[1:] +
                              "/status/" + str(tweet[1]), 'yellow'))

        if not found_tweet:
            print(colored("[*] I couldn't find a tweet like that. " +
                          "Try increasing the limit to pull more tweets",
                          'yellow'))

    except TwitterSearchException as e:  # catch all those ugly errors
        print(e)


def _blow_up_image():
    try:
        img = Image.open(args.image)
    except (OSError, IOError):
        print(colored("[!] I couldn't find a file by that name. Fake you!",
                      'red'))
        return False

    basewidth = 2500
    img = Image.open(args.image)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    # Resize happens here
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

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
