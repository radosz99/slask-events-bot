import requests

from constants import DEBUG, DEBUG_MESSAGE
from secrets import SMS_API_URL, SMS_REQUEST_DETAILS
from utils import log_message


def notify_user_about_the_event_via_sms(event):
    sms_content = event.sms_content()
    log_message(f"Preparing SMS: \n {sms_content} \n")
    SMS_REQUEST_DETAILS['msg'] = sms_content
    return send_sms(SMS_REQUEST_DETAILS)


def send_sms(sms_details):
    response_json = send_sms_via_smsplanet_api(sms_details)
    if "messageId" in response_json:
        increment_sms_sent_number()
        log_message(f"Message has been sent, id = {response_json['messageId']}, debug mode = {DEBUG}")
        return True
    else:
        log_message(f"Message has not been sent due to an error, probably not enough points on sms planet platform - "
                    f"{response_json}")
        return False


def sms_limit_exceeded():
    import constants
    if constants.TOTAL_SMS_SENT < constants.SMS_LIMIT:
        log_message(f"SMS limit has not been exceeded, {constants.TOTAL_SMS_SENT} < {constants.SMS_LIMIT}")
        return True
    else:
        log_message(f"SMS limit has been exceeded, {constants.TOTAL_SMS_SENT} >= {constants.SMS_LIMIT}")
        return False


def increment_sms_sent_number():
    import constants
    constants.TOTAL_SMS_SENT += 1
    log_message(f"Incrementing SMS sent total number, current = {constants.TOTAL_SMS_SENT}")


def send_sms_via_smsplanet_api(sms_details):
    if not DEBUG and sms_limit_exceeded():
        log_message("Trying to send SMS")
        return requests.get(SMS_API_URL, params=sms_details).json()
    else:
        return DEBUG_MESSAGE
