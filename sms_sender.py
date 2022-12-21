from constants import DEBUG, DEBUG_MESSAGE
import smsplanet_api
from logger import logger


def notify_user_about_the_event_via_sms(event):
    sms_content = event.sms_content()
    logger.info(f"Prepared SMS with length = {len(sms_content)}: \n {sms_content} \n")
    return send_sms_and_validate(sms_content)


def send_sms_and_validate(sms_content):
    response_json = send_sms_via_smsplanet_api(sms_content)
    if "messageId" in response_json:
        increment_sms_sent_number()
        logger.info(f"Message has been sent, id = {response_json['messageId']}, debug mode = {DEBUG}")
        return True
    else:
        logger.info(f"Message has not been sent due to an error, probably not enough points on sms planet platform - "
                    f"{response_json}")
        return False


def sms_limit_exceeded():
    import constants
    if constants.TOTAL_SMS_SENT < constants.SMS_LIMIT:
        logger.info(f"SMS limit has not been exceeded, {constants.TOTAL_SMS_SENT} < {constants.SMS_LIMIT}")
        return True
    else:
        logger.info(f"SMS limit has been exceeded, {constants.TOTAL_SMS_SENT} >= {constants.SMS_LIMIT}")
        return False


def increment_sms_sent_number():
    import constants
    constants.TOTAL_SMS_SENT += 1
    logger.info(f"Incrementing SMS sent total number, current = {constants.TOTAL_SMS_SENT}")


def send_sms_via_smsplanet_api(sms_content):
    if not DEBUG and sms_limit_exceeded():
        logger.info("Trying to send SMS")
        return smsplanet_api.send_sms_via_get_method(sms_content)
    else:
        return DEBUG_MESSAGE
