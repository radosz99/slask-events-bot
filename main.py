import traceback
from time import sleep

from utils import get_driver, log_message, get_slask_events, get_new_elements_on_list
from sms_sender import notify_user_about_the_event_via_sms
from constants import SKIP_FIRST_LOOP, SCAN_PERIOD


def notify_user_about_new_event(new_event):
    user_notified = notify_user_about_the_event_via_sms(new_event)
    if user_notified:
        log_message("User has been notified about the event")
    else:
        log_message("User has not been notified for some reason")


def notify_user_about_new_event_if_first_team_is_playing(new_event):
    if not new_event.slask_first_team_event():
        log_message("Not the first team game, SMS will not be send")
    elif not new_event.tickets_available():
        log_message("First team game, but tickets are not available yet, SMS will not be send")
    else:
        log_message("It is the first team game with active tickets url, SMS will be send")
        notify_user_about_new_event(new_event)


def notify_user_if_new_events_have_appeared(latest_events, current_events):
    new_events = get_new_elements_on_list(current_events, latest_events)
    if new_events:
        log_message(f"List of events has changed, old events = {latest_events}, current events = {current_events}")
        for new_event in new_events:
            log_message(f"New event - {new_event}")
            notify_user_about_new_event_if_first_team_is_playing(new_event)
    else:
        log_message("Nothing has changed, no new events :(")


def main():
    latest_events = []
    while True:
        driver = get_driver(headless=True)
        try:
            log_message("Getting new driver and fetching Slask Wroclaw events")
            events = get_slask_events(driver)
            if not latest_events and SKIP_FIRST_LOOP:
                log_message(f"First loop iteration, current events = {events}")
            else:
                notify_user_if_new_events_have_appeared(latest_events, events)
            latest_events = events
        except Exception:
            log_message(f"Exception has occurred = {traceback.format_exc()}")
        finally:
            log_message(f"Quitting the driver and sleeping for {SCAN_PERIOD} seconds")
            driver.quit()
            sleep(SCAN_PERIOD)


if __name__ == '__main__':
    main()

