TICKETS_WEBSITE = "http://wks-slask.abilet.pl/"
XPATHS = {
    "event_row": ".//section[@id='bilety']//div[@class='row']",
    "place": ".//p[@class='card-place text-center']",
    "date": ".//p[@class='card-date font-weight-bold text-center']",
    "title": ".//p[@class='card-title text-center']",
    "tickets_url": ".//a[@class='btn btn-block btn-info font-weight-bold']"
}
SCAN_PERIOD = 120
DEBUG = True  # set to True to avoid sending real sms
DEBUG_MESSAGE = {"messageId": "16054772"}
SMS_LIMIT = 5
TOTAL_SMS_SENT = 0
LOG_FILE = "debug.log"
