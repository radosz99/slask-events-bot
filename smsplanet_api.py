import requests
import logging

from secrets import SEND_SMS_API, CUT_URL_API, API_KEY, API_KEY_PASS, PHONE_NUMBER, SENDER_NAME
from logger import logger


def log_message(string, level=logging.INFO):
    logger.log(level, string)


def send_sms_via_get_method(content):
    sms_details = {'to': PHONE_NUMBER,
                   'key': API_KEY,
                   'password': API_KEY_PASS,
                   'from': SENDER_NAME,
                   'msg': content}
    log_message(f"Sending SMS via sms planet API with details = {sms_details}")
    response_json = requests.get(SEND_SMS_API, params=sms_details).json()
    log_message(f"Response = {response_json}")
    return response_json


def cut_url(long_url):
    cut_url_details = {
        'longUrl': long_url,
        'key': API_KEY,
        'password': API_KEY_PASS}
    log_message(f"Cutting URL via sms planet API with details = {cut_url_details}")
    response_json = requests.post(CUT_URL_API, params=cut_url_details).json()
    log_message(f"Response = {response_json}")
    return response_json
