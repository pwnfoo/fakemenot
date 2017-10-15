import argparse
import os
import sys
import configparser
from TwitterSearch import *
from termcolor import colored

from fakemenot.ocr import find_user_and_text_in_tweet_image

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


def _do_lookup(potential_user, body):
    config = get_config()
    limit_of_tweets = int(args.limit)

    # Just in case the person using the program puts in ' or " in the config.
    consumer_key = config.get(
        'twitter',
        'consumer_key').replace(
        '\'', '').replace(
        '\"', '')
    consumer_secret = config.get(
        'twitter',
        'consumer_secret').replace(
        '\'', '').replace(
        '\"', '')
    access_token = config.get(
        'twitter',
        'access_token').replace(
        '\'', '').replace(
        '\"', '')
    access_token_secret = config.get(
        'twitter',
        'access_token_secret').replace(
        '\'', '').replace(
        '\"', '')

    if potential_user is None:
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
        for tweet in ts.search_tweets_iterable(tuo):
            # Nobody cares about re-tweets
            if 'RT ' not in tweet['text']:
                if tweet not in tweets:
                    tweets.append((tweet['text'], tweet['id']))
                if not limit_of_tweets:
                    break
                else:
                    limit_of_tweets -= 1

        # If none of that was found, let's report an OCR error
        if body is None:
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

            if int(removal_rate) > 75:
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


def main():
    user, tweet_text = find_user_and_text_in_tweet_image(args.image)
    _do_lookup(user, tweet_text)


if __name__ == '__main__':
    main()
