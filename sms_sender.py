from constants import DEBUG, DEBUG_MESSAGE
from utils import log_message
import smsplanet_api
import exceptions as exc


def notify_user_about_the_event_via_sms(event):
    try:
        sms_content = event.sms_content()
        log_message(f"Prepared SMS with length = {len(sms_content)}: \n {sms_content} \n")
        send_sms(sms_content)
        log_message("User has been notified about the event")
    except exc.SMSHasNotBeenSentError as e:
        log_message(f"User has not been notified for some reason - {e}")


def send_sms(sms_content):
    check_if_sms_limit_has_been_exceeded()
    response_json = send_sms_via_smsplanet_api(sms_content)
    validate_response_after_sending_sms(response_json)


def check_if_sms_limit_has_been_exceeded():
    import constants
    if constants.TOTAL_SMS_SENT < constants.SMS_LIMIT:
        log_message(f"SMS limit has not been exceeded, {constants.TOTAL_SMS_SENT} < {constants.SMS_LIMIT}")
    else:
        msg = f"SMS limit has been exceeded, {constants.TOTAL_SMS_SENT} >= {constants.SMS_LIMIT}"
        log_message(msg)
        raise exc.SMSHasNotBeenSentError(msg)


def validate_response_after_sending_sms(response):
    if "messageId" in response:
        increment_sms_sent_number()
        log_message(f"Message has been sent, id = {response['messageId']}, debug mode = {DEBUG}")
    else:
        msg = f"Message has not been sent due to an error, probably not enough credits on your sms planet account - " \
              f"{response}"
        log_message(msg)
        raise exc.SMSHasNotBeenSentError(msg)


def increment_sms_sent_number():
    import constants
    constants.TOTAL_SMS_SENT += 1
    log_message(f"Incrementing SMS sent total number, current = {constants.TOTAL_SMS_SENT}")


def send_sms_via_smsplanet_api(sms_content):
    if not DEBUG:
        log_message("Trying to send SMS")
        return smsplanet_api.send_sms_via_get_method(sms_content)
    else:
        return DEBUG_MESSAGE
