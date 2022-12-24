import re

from urllib.request import urlopen
from lxml import etree
from typing import List

from constants import XPATHS, TICKETS_URL, SMS_LENGTH_LIMIT
from logger import logger
import smsplanet_api


def get_attribute_value_from_element_by_xpath(element: etree._Element, xpath, attribute_name):
    try:
        return element.xpath(xpath)[0].get(attribute_name)
    except IndexError:
        return None


def remove_accents(string):
    strange = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
    ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'

    translator = str.maketrans(strange, ascii_replacements)

    return string.translate(translator)


def get_text_inside_element_by_xpath(element, xpath):
    try:
        text = element.xpath(xpath)[0].text
        text_without_accents = remove_accents(text)
        return text_without_accents
    except IndexError:
        return None


def get_tickets_url_from_event(event_element):
    return get_attribute_value_from_element_by_xpath(event_element, XPATHS['tickets_url'], 'href')


def get_name_from_event(event_element):
    return get_text_inside_element_by_xpath(event_element, XPATHS['title'])


def get_date_from_event(event_element):
    date = get_text_inside_element_by_xpath(event_element, XPATHS['date'])
    date = date.replace('\n', ' ').replace('\r', '').lstrip().rstrip()
    return re.sub(' +', ' ', date)


def get_place_from_event(event_element):
    return get_text_inside_element_by_xpath(event_element, XPATHS['place'])


class Event:
    def __init__(self, **kwargs):
        if event := kwargs.get('lxml_event', None):
            self._create_from_lxml_element(event)
        else:
            self._create_from_arguments(kwargs)

    def _create_from_arguments(self, arguments_dict):
        self.name = arguments_dict.get('name', None)
        self.place = arguments_dict.get('place', None)
        self.date = arguments_dict.get('date', None)
        self.tickets_url = arguments_dict.get('tickets_url', None)
        self.tickets_url_2 = self.get_better_tickets_url()

    def _create_from_lxml_element(self, event):
        self.place = get_place_from_event(event)
        self.name = get_name_from_event(event)
        self.date = get_date_from_event(event)
        self.tickets_url = get_tickets_url_from_event(event)
        self.tickets_url_2 = self.get_better_tickets_url()

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
        return self.name == other.name and self.date == other.date and self.place == other.place

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
        logger.info(f"Prepared content with length = {len(content)}: {content}")
        return content

    def sms_content_under_limit(self):
        short_url = cut_url_via_smsplanet_api(self.tickets_url_2)
        content = f"Tickets for {self.name} on {self.date} in {self.place}: - {short_url}"
        if len(content) < SMS_LENGTH_LIMIT:
            return content
        else:
            return f"Tickets for {self.name}: - {short_url}"


def get_slask_events():
    tree = etree.parse(urlopen(TICKETS_URL), etree.HTMLParser())
    return [Event(lxml_event=event) for event in tree.xpath(XPATHS["event_row"])]


def get_new_events(current_events: List[Event], previous_events: List[Event]):
    logger.debug("Getting new events")
    new_events = []
    for current_event in current_events:
        logger.debug(f"Checking event: {current_event}")
        for previous_event in previous_events:
            if current_event == previous_event:
                logger.debug(f"Probably not a new event, but checking if the tickets url has been updated from None, "
                             f"corresponding previous event: {previous_event}")
                if current_event.tickets_url and not previous_event.tickets_url:
                    logger.debug(f"New event, tickets url was updated from {previous_event.tickets_url} to "
                                 f"{current_event.tickets_url}, adding to new events list")
                    new_events.append(current_event)  # add if the same, but tickets url has been updated from None
                break  # stop checking previous events list because the same event is on current events list
        else:
            logger.debug("Completely nww event, adding to new events list")
            new_events.append(current_event)  # add if event is not equal to any from previous events list
    logger.debug(f"New events = {new_events}")
    return new_events


def cut_url_via_smsplanet_api(url):
    logger.info(f"Cutting url '{url}' via sms planet api")
    short_url = smsplanet_api.get_truncated_url(url)
    logger.info(f"URL has been cut to '{short_url}'")
    return short_url

