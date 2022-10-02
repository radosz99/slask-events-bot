import traceback
from time import sleep

from utils import get_driver, log_message, get_slask_events, get_new_elements_on_list
from sms_sender import notify_user_about_the_event_via_sms


def notify_user_about_new_event(new_event):
    user_notified = notify_user_about_the_event_via_sms(new_event)
    if user_notified:
        log_message("User has been notified about the event")
    else:
        log_message("User has not been notified for some reason")


def notify_user_about_new_event_if_first_team_is_playing(new_event):
    if new_event.slask_first_team_event():
        log_message("It is the first team event, SMS will be send")
        notify_user_about_new_event(new_event)
    else:
        log_message("Not the first team event, no SMS will be send")


def notify_user_if_new_events_have_appeared(latest_events, current_events):
    if current_events != latest_events:
        log_message("New event have appeared")
        for new_event in get_new_elements_on_list(current_events, latest_events):
            log_message(f"New event - {new_event}")
            notify_user_about_new_event_if_first_team_is_playing(new_event)
    else:
        log_message("Nothing has changed, old events :(")


def main():
    latest_events = []
    while True:
        driver = get_driver(headless=True)
        try:
            log_message("Getting new driver and fetching Slask Wroclaw events")
            events = get_slask_events(driver)
            notify_user_if_new_events_have_appeared(latest_events, events)
            latest_events = events
        except Exception:
            log_message(f"Exception has occurred = {traceback.format_exc()}")
        finally:
            from constants import SCAN_PERIOD
            log_message(f"Quitting the driver and sleeping for {SCAN_PERIOD} seconds")
            driver.quit()
            sleep(SCAN_PERIOD)


if __name__ == '__main__':
    main()

