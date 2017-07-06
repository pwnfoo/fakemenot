# fakemenot
Python CLI app to detect if a screenshot of a tweet is genuine. Work in Progress

### Requriements

* tesseract
* tesseract-data-eng

### Setting Up

* Run `python setup.py install` to install requirements. Install script is still a work in progress.
* Run `python fakemenot/app.py` after installation.


### Arguments

* `--image/-i`

Path to the screenshot image of tweet. Only works on Desktop screenshots.

* `--limit/-l`

Specify the number of tweets to pull from the detected user. Defaults to 100. Retweets are not pulled.


### Image Samples 

Tweet by @mattdm: 

![](http://i.imgur.com/5oDeoxv.png)

Output:

![](http://i.imgur.com/05ZeCxL.png)
