import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from constants import XPATHS, TICKETS_WEBSITE
from logger import logger


def get_attribute_value_from_element_by_xpath(selenium_element, xpath, attribute_name):
    try:
        return selenium_element.find_element(By.XPATH, xpath).get_attribute(attribute_name)
    except NoSuchElementException:
        return None


def get_text_inside_element_by_xpath(selenium_element, xpath):
    try:
        return selenium_element.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return None


def get_tickets_url_from_event(event_element):
    return get_attribute_value_from_element_by_xpath(event_element, XPATHS['tickets_url'], 'href')


def get_name_from_event(event_element):
    return get_text_inside_element_by_xpath(event_element, XPATHS['title'])


def get_date_from_event(event_element):
    return get_text_inside_element_by_xpath(event_element, XPATHS['date'])


def get_place_from_event(event_element):
    return get_text_inside_element_by_xpath(event_element, XPATHS['place'])


def log_message(string, level=logging.INFO):
    logger.log(level, string)


def get_new_elements_on_list(new_list, old_list):
    return list(set(new_list) - set(old_list))


class Event:
    def __init__(self, event):
        self.name = get_name_from_event(event)
        self.place = get_place_from_event(event)
        self.date = get_date_from_event(event)
        self.tickets_url = get_tickets_url_from_event(event)
        self.tickets_url_2 = self.get_better_tickets_url()

    def __key(self):
        return self.name, self.place, self.date

    def get_better_tickets_url(self):
        return self.tickets_url.replace('impreza', 'sala')

    def __str__(self):
        return f"Title = {self.name} will take place in {self.place} on {self.date}, first team = " \
               f"{self.slask_first_team_event()}, tickets url = {self.tickets_url_2}"

    def __eq__(self, other):
        return self.name == other.name and self.date == other.date and self.place == other.place

    def __hash__(self):
        return hash(self.__key())

    def slask_first_team_event(self):
        return "WKS Śląsk Wrocław" in self.name and "vs" in self.name

    def sms_content(self):
        # return f"Tickets for {self.name} on {self.date} in {self.place} are now available here - {self.tickets_url_2}"
        return f"Tickets for {self.name} on {self.date} in {self.place} are now available"


def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    return webdriver.Firefox(options=options)


def get_slask_events(driver):
    driver.get(TICKETS_WEBSITE)
    return [Event(event_row) for event_row in driver.find_elements(By.XPATH, XPATHS['event_row'])]
