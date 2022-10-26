import traceback
from time import sleep

from utils import get_driver, log_message, get_slask_events, get_new_elements_on_list, modify_scan_period, get_scan_period
from sms_sender import notify_user_about_the_event_via_sms
import exceptions as exc


def notify_user_about_new_event(new_event):
    notify_user_about_the_event_via_sms(new_event)


def notify_user_about_new_event_if_first_team_is_playing(new_event):
    if new_event.slask_first_team_event():
        log_message("It is the first team game, SMS will be send")
        notify_user_about_new_event(new_event)
    else:
        log_message("Not the first team game, no SMS will be send")


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
            if latest_events:
                notify_user_if_new_events_have_appeared(latest_events, events)
            else:
                log_message(f"First loop iteration, current events = {events}")
            latest_events = events
            modify_scan_period(normal=True)
        except exc.URLNotAvailableError:
            modify_scan_period(normal=False)
        except Exception:
            log_message(f"Exception has occurred = {traceback.format_exc()}")
        finally:
            scan_period = get_scan_period()
            log_message(f"Quitting the driver and sleeping for {scan_period} seconds")
            driver.quit()
            sleep(scan_period)


if __name__ == '__main__':
    main()

