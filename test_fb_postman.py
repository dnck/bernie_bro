import time

import fb_postman

if __name__ == "__main__":
    poster = fb_postman.FBPostMan()
    poster.set_up()
    poster.login()
    poster.post_news(msg="This is a test!")
    time.sleep(1)
    poster.tear_down()