# Introduction

`bernie_bro.py` searches for recent news articles from Washington Post, NPR, NYTimes, and Reuters. When the articles are related to Trump or Sanders, it ranks the article for sentiment. If the Trump sentiment is negative, it shares a message and the link to the article on the user's FB homepage. If the Sanders sentiment is positive, it shares a message and the link to the article on the user's FB page. It posts only 1 message and 1 article per person per run. It can therefore be set up in a cron job to run multiple times a day, week, month, etc.
  
:heavy_check_mark: Vote for Bernie Sanders!
  

## Requirement

### python >= 3.7

On Linux/Ubuntu/Raspberry Pi:
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc && \
source ~/.bashrc && \
pyenv install 3.8.0 && \
pyenv global 3.8.0 && \
python --version
```
On MacOS Catalina:
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshenv && \
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshenv && \
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshenv && 
source ~/.zshenv && \
pyenv install 3.8.0 && \
pyenv global 3.8.0 && \
python --version
```


###  Firefox browser (or on Raspberry pi, firefox erf)

```
sudo apt-get install firefox-esr
```

### geckodriver
On macOs, download unpack and mv the binary to /usr/local/bin:
https://github.com/mozilla/geckodriver/releases/tag/v0.25.0
On Raspberry pi, download unpack and mv the binary to /usr/local/bin:
```
wget -o https://github.com/mozilla/geckodriver/releases/download/v0.22.0/geckodriver-v0.22.0-arm7hf.tar.gz
```
## Quickstart 

```
git clone https://github.com/dnck/bernie_bro.git && \
cd bernie_bro && \
python -m venv . && \
source bin/activate && \
pip install -r requirements.txt && \
touch .env
```
Now create your local `.env` file to store secrets.
```
EMAIL=<your-fb-email-address>
PASSWORD=<your-fb-password>
TWITTER_A_TOKEN=<twitter-access-token>
TWITTER_A_SECRET=<twitter-access-secret>
TWITTER_C_TOKEN=<twitter-consumer-token>
TWITTER_C_SECRET=<twitter-consumer-secret>
TWITTER_NAME=<twitter-name>
```
For explanations on how to get the twitter tokens and secrets, see:
http://docs.tweepy.org/en/v3.8.0/getting_started.html

Even without the twitter tokens, you can run a test of the fb_postman:
```
python ./test_fb_postman.py
```

To set up a recurring cron job for bernie_bro, on a Linux system, 
make a crontab entry:

Using,
```
crontab -e
```
Enter, 
```
0 10 * * *  /home/<username>/MySocialMan/vote_bernie.sh
```

Every morning at 10am, bernie_bro will post for you.