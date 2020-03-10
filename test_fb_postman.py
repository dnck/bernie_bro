import time

import fb_postman

if __name__ == "__main__":
    poster = fb_postman.FBPostMan()
    poster.set_up()
    poster.login()
    poster.post_news(msg="This is a test! https://www.washingtonpost.com/health/2020/03/10/social-distancing-coronavirus/ ")
    time.sleep(1)
    poster.tear_down()