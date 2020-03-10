import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

USER = None
PASS = None

def get_secrets():
    global USER, PASS
    PY_DIRNAME, PY_FILENAME = os.path.split(os.path.abspath(__file__))
    ENV_FILE = os.path.join(PY_DIRNAME, ".env")
    load_dotenv(dotenv_path=ENV_FILE)
    USER = os.environ.get("EMAIL")
    PASS = os.environ.get("PASSWORD")

class FBPostMan():

    def __init__(self):
        get_secrets()
        self.edit_post_box_syntax =  \
            "//textarea[contains(@aria-label, 'on your mind')]"
        self.post_button_syntax = \
            "//div[@id='pagelet_composer']//button[@type='submit']"        
        self.logged_in = False

    def set_up(self):
        options = Options()
        options.add_argument("--headless")
        options.set_preference("dom.webnotifications.enabled", False)
        self.browser = webdriver.Firefox(options=options)

    def tear_down(self):
        self.browser.quit()

    def login(self):
        """
        Login to Facebook as user
        """
        self.browser.get("https://www.facebook.com/login")
        email_input = self.browser.find_element_by_id("email")
        email_input.send_keys(USER)
        pass_input = self.browser.find_element_by_id("pass")
        pass_input.send_keys(PASS)
        login_button = self.browser.find_element_by_id("loginbutton")
        login_button.click()
        time.sleep(2)
        self.logged_in = True

    def post_news(self, msg):
        """
        Post a message to the logged-in user's newsfeed
        """
        if not self.logged_in:
            raise ValueError("User must be logged to use this feature.")
        post_box=self.browser.find_element_by_xpath(self.edit_post_box_syntax)
        post_box.send_keys(msg)
        time.sleep(6)
        try:
            post_button = \
                self.browser.find_element_by_xpath(self.post_button_syntax)
            if post_button:
                #print(post_button)
                post_button.click()
        except:
            print("Could not find button.")
