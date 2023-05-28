TICKETS_URL = "https://kingwilki.abilet.pl/"
XPATHS = {
    "event_row": ".//section[@id='bilety']//div[@class='row']",
    "place": ".//p[@class='card-place text-center']",
    "date": ".//p[@class='card-date font-weight-bold text-center']",
    "title": ".//p[@class='card-title text-center']",
    "tickets_url": ".//a[@class='btn btn-block btn-info font-weight-bold']"
}
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

SCAN_PERIOD = 30  # time of sleeping in a loop
DEBUG_LOG_FILE = "debug.log"
INFO_LOG_FILE = "info.log"
SKIP_FIRST_LOOP = True

DEBUG = True  # set to True to avoid sending real sms
DEBUG_MESSAGE = {"messageId": "DEBUG MODE IS ON"}  # this mocked response will be sent if DEBUG = True

SMS_LIMIT = 5  # maximum amount of SMS to send from SMS planet API for avoiding bankruptcy
TOTAL_SMS_SENT = 0  # for checking if limit has been exceeded
SMS_LENGTH_LIMIT = 160  # maximum SMS content length above which content will be truncated
