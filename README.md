# Info

Python application for notifying when tickets for new event of Slask Wroclaw basketball team appeared on [this](http://wks-slask.abilet.pl/) page.  

<p align="center">
  <img src="https://github.com/radosz99/slask-events-bot/blob/main/screen.png" width=30% alt="Img"/>
</p>

## Detail info
The application is running as a Docker daemon with Python script in it which checks content of the page with tickets. In a loop it scraps current events for which tickets are available and compares with the previously scrapped events. If some changes occurred then SMS notification with specially prepared content is sent according to the `secrets.py` file.  

The goal of this application is to have an option to buy tickets with the best seats for matches. This works because the ticket URL is published later on the official fanpage and many people refresh the page manually.
[SMSPLANET](https://smsplanet.pl/) is used for SMS notification. 

## Tech stack
- Python 3.8,
- Docker,
- Selenium.

# Installation and running
First of all clone the repository.

## Creating account on SMSPLANET
Create an account [here](https://panel.smsplanet.pl/register) and top up your balance. In [sender page](https://panel.smsplanet.pl/s/sender) create your own sender name, which will appear in the SMS as the sender.

## Secrets.py file
In a root directory of the repository place an `secrets.py` file with following content:
```
SMS_PLANET_API_URL = "https://api2.smsplanet.pl"
SEND_SMS_API = f"{SMS_PLANET_API_URL}/sms"
CUT_URL_API = f"{SMS_PLANET_API_URL}/shortUrl"
API_KEY = "YOUR-KEY"
API_KEY_PASS = "YOUR-KEY-PASSWORD"
PHONE_NUMBER = YOUR-PHONE-NUMBER
SENDER_NAME = "YOUR-SENDER-NAME"
```
Modify variables `API_KEY` and `API_KEY_PASS` with values from [here](https://panel.smsplanet.pl/s/api). As a `PHONE_NUMBER` type your own number, note that the country code is optional. As a `SENDER_NAME` type your created previously name, note you should wait for acceptation from the SMSPLANET.

## Constants.py file
Some variables in `constants.py` file are modifiable:
```
...
SCAN_PERIOD = 30  # time of sleeping in a loop
LOG_FILE = "debug.log"

DEBUG = True  # set to True to avoid sending real sms
DEBUG_MESSAGE = {"messageId": "DEBUG MODE IS ON"}  # this mocked response will be sent if DEBUG = True

SMS_LIMIT = 5  # maximum amount of SMS to send from SMS planet API for avoiding bankruptcy
TOTAL_SMS_SENT = 0  # for checking if limit has been exceeded
SMS_LENGTH_LIMIT = 160  # maximum SMS content length above which content will be truncated
```
To debug the application just set `DEBUG` to `True` and real SMS will not be sent.

## Run run.sh bash script
Add execution permission to `run.sh` script and run it. It will run Docker daemon which will scrap data each `SCAN_PERIOD` seconds.
# To do

- [ ] - consider moving from Selenium to Urllib + BeautifulSoup since only page source is used
