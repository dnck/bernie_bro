import time

import fb_postman

"""
This little script shows you how to infinitely scroll on a facebook page after
you log in. More intricate methods can be hacked together to let you scrap 
you frenemies page. You can then of course create a profile of your frenemies
using whatever episonage tactic you like.
"""
class FbPoster():
    def __init__(self):
        self.poster = fb_postman.FBPostMan()
        
    def simulate_dr_connell(self):
        self.poster.set_up()
        print(1)
        self.poster.login()
        self.scroll()
        time.sleep(1)
        self.poster.tear_down()
        
    def scroll(self):
        self.poster.browser.get("https://www.facebook.com/TheRubberbandits/")
        SCROLL_PAUSE_TIME = 5.0
        # Get scroll height
        last_height = self.poster.browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.poster.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.poster.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
if __name__ == "__main__":
    garrett = FbPoster()
    garrett.simulate_dr_connell()