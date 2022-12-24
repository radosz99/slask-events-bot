import traceback
from time import sleep

from utils import get_slask_events, get_new_events
from sms_sender import notify_user_about_the_event_via_sms
from constants import SKIP_FIRST_LOOP, SCAN_PERIOD
from logger import logger


def notify_user_about_new_event(new_event):
    user_notified = notify_user_about_the_event_via_sms(new_event)
    if user_notified:
        logger.info("User has been notified about the event")
    else:
        logger.info("User has not been notified for some reason")


def notify_user_about_new_event_if_first_team_is_playing(new_event):
    if not new_event.slask_first_team_event():
        logger.info("Not the first team game, SMS will not be send")
    elif not new_event.tickets_available():
        logger.info("First team game, but tickets are not available yet, SMS will not be send")
    else:
        logger.info("It is the first team game with active tickets url, SMS will be send")
        notify_user_about_new_event(new_event)


def notify_user_if_new_events_have_appeared(previous_events, current_events):
    new_events = get_new_events(current_events, previous_events)
    if new_events:
        logger.info(f"List of events has changed, previous events = {previous_events}, current events = {current_events}")
        for new_event in new_events:
            logger.info(f"New event - {new_event}")
            notify_user_about_new_event_if_first_team_is_playing(new_event)
        return True
    else:
        logger.info("Nothing has changed, no new events :(")
        return False


def main():
    latest_events = []
    while True:
        try:
            logger.info("Fetching Slask Wroclaw events")
            events = get_slask_events()
            if not latest_events and SKIP_FIRST_LOOP:
                logger.info(f"First loop iteration, current events = {events}")
                latest_events = events
            else:
                if notify_user_if_new_events_have_appeared(latest_events, events):
                    latest_events = events
        except Exception:
            logger.error(f"Exception has occurred = {traceback.format_exc()}")
        finally:
            logger.info(f"Sleeping for {SCAN_PERIOD} seconds")
            sleep(SCAN_PERIOD)


if __name__ == '__main__':
    main()

