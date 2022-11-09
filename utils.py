import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from constants import XPATHS, TICKETS_WEBSITE, SMS_LENGTH_LIMIT
from logger import logger
import smsplanet_api


def get_attribute_value_from_element_by_xpath(selenium_element, xpath, attribute_name):
    try:
        return selenium_element.find_element(By.XPATH, xpath).get_attribute(attribute_name)
    except NoSuchElementException:
        return None


def remove_accents(string):
    strange = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
    ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'

    translator = str.maketrans(strange, ascii_replacements)

    return string.translate(translator)


def get_text_inside_element_by_xpath(selenium_element, xpath):
    try:
        text = selenium_element.find_element(By.XPATH, xpath).text
        text_without_accents = remove_accents(text)
        return text_without_accents
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
    def __init__(self, **kwargs):
        event = kwargs.get('selenium_event', None)
        if event is not None:
            self._create_from_selenium_element(event)
        else:
            self._create_from_arguments(kwargs)

    def _create_from_selenium_element(self, event):
        self.name = get_name_from_event(event)
        self.place = get_place_from_event(event)
        self.date = get_date_from_event(event)
        self.tickets_url = get_tickets_url_from_event(event)
        self.tickets_url_2 = self.get_better_tickets_url()

    def _create_from_arguments(self, arguments_dict):
        self.name = arguments_dict.get('name', None)
        self.place = arguments_dict.get('place', None)
        self.date = arguments_dict.get('date', None)
        self.tickets_url = arguments_dict.get('tickets_url', None)
        self.tickets_url_2 = self.get_better_tickets_url()

    def __key(self):
        return self.name, self.place, self.date, self.tickets_url

    def get_better_tickets_url(self):
        try:
            return self.tickets_url.replace('impreza', 'sala')
        except Exception:
            return self.tickets_url

    def __str__(self):
        return f"Title = {self.name} will take place in {self.place} on {self.date}, first team = " \
               f"{self.slask_first_team_game()}, tickets url = {self.tickets_url_2}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.date == other.date and self.place == other.place \
               and self.tickets_url == other.tickets_url

    def __hash__(self):
        return hash(self.__key())

    def slask_first_team_game(self):
        return self.slask_first_team_event() and self.game_event()

    def tickets_available(self):
        return self.tickets_url is not None

    def slask_first_team_event(self):
        return "WKS Slask Wroclaw" in self.name

    def game_event(self):
        return "vs" in self.name

    def sms_content(self):
        content = self.sms_content_under_limit()
        log_message(f"Prepared content with length = {len(content)}: {content}")
        return content

    def sms_content_under_limit(self):
        short_url = cut_url_via_smsplanet_api(self.tickets_url_2)
        content = f"Tickets for {self.name} on {self.date} in {self.place}: - {short_url}"
        if len(content) < SMS_LENGTH_LIMIT:
            return content
        else:
            return f"Tickets for {self.name}: - {short_url}"


def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    return webdriver.Firefox(options=options)


def get_slask_events(driver):
    driver.get(TICKETS_WEBSITE)
    return [Event(selenium_event=event_row) for event_row in driver.find_elements(By.XPATH, XPATHS['event_row'])]


def cut_url_via_smsplanet_api(url):
    log_message(f"Cutting url '{url}' via sms planet api")
    short_url = smsplanet_api.get_truncated_url(url)
    log_message(f"URL has been cut to '{short_url}'")
    return short_url

