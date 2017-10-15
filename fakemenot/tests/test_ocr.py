import unittest
from difflib import SequenceMatcher
from fakemenot.ocr import find_user_and_text_in_tweet_image


class OcrTestCase(unittest.TestCase):
    def common_test_ocr_tweet(self, image_path, expected_user, expected_text):
        user, text = find_user_and_text_in_tweet_image(image_path)
        self.assertEqual(expected_user, user)
        self.assertTrue(SequenceMatcher(a=expected_text, b=text).ratio() > 0.95)

    def test_ocr_tweet_1(self):
        expected_user = "@mattdm"
        expected_text = "Got bored so updated my #fedora 25 laptop to pre-alpha 26. Started, went for lunch, came " \
                        "back to a system which Just Works -- no fuss!"
        self.common_test_ocr_tweet("res/test_ocr_1.png", expected_user, expected_text)

    def test_ocr_tweet_2(self):
        expected_user = "@NASA"
        expected_text = "For 70 years, planes loudly flew supersonic & barriers were broken. Now we're making " \
                        "history again in a quiet way: go.nasa.gov/2kOO1cc"
        self.common_test_ocr_tweet("res/test_ocr_2.png", expected_user, expected_text)

    def test_ocr_tweet_3(self):
        expected_user = "@wikileaks"
        expected_text = "Harvard made Harry Belafonte & Ira Berlin share its highest honor in African American " \
                        "Studies with Harvey Weinstein"
        self.common_test_ocr_tweet("res/test_ocr_3.png", expected_user, expected_text)


if __name__ == '__main__':
    unittest.main()
