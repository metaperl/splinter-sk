#!/usr/bin/python

import pdb

from splinter import Browser

user = dict(
    email = "schemelab@gmail.com",
    first_name = "Terrence",
    last_name = "Brannon",
    phone_number = "818-359-0893",
    address = "713 Chadford Rd",
    city = "Irmo",
    state = "usa-sc",
    zip = "29063"
)

base_url = 'http://www.sheknows.com'

def contest_urls(browser):
    contests = browser.find_by_xpath('//*[@id="carousel_list"]/li')
    urls = [ contest_url(contest['data-url']) for contest in contests ]
    u = [x for x in urls if "pin-spiration" not in x]
    return u

def contest_url(path):
    return "{0}{1}".format(base_url,path)


class ContestEntry(object):

    @staticmethod
    def mystyle(url):
        return "singlehood" in url

    def __init__(self, browser, url):
        self.browser=browser
        self.url=url
        self.email_name_attribute = "data[GiveawayEntry][email]"

    def submit_contact_info(self):
        button = self.browser.find_by_xpath('//*[@class="submit button"]')
        button.click()

    def _enter_email(self):
        self.browser.fill(self.email_name_attribute, user['email'])

    def enter_email(self):
        self._enter_email()
        self.click_submit()

    def enter_contact_info(self):
        for k, v in user.items():
            if k == 'state': continue
            field_name = "data[GiveawayEntry][{0}]".format(k)
            if k == 'address' or k == 'city' or k == 'zip':
                field_name = "data[GiveawayEntryAddress][{0}]".format(k)
            self.browser.fill(field_name, v)
        e = self.browser.find_by_xpath(
            '//*[@value="{0}"]'.format(user['state'])
        )
        e._element.click()
        self.submit_contact_info()

    def confirm_info(self):
        self.browser.find_by_xpath('//*[@class="button button-yes"]').click()

    def find_accept_button(self):
        return self.browser.find_by_xpath('//*[@class="button"]').click()

    def accept_terms(self):
        button = self.find_accept_button()
        button.click()


    def enter_contest(self):
        print "\tEntering contest {0}".format(self.url)
        self.browser.visit(self.url)
        self.enter_email()
        self.enter_contact_info()
        self.confirm_info()
        self.accept_terms()

class ContestEntry2(ContestEntry):

    @staticmethod
    def mystyle(url):
        return "500-happy" in url

    def __init__(self, browser, url):
        super(ContestEntry2, self).__init__(browser, url)

    def click_submit(self):
        button = self.browser.find_by_xpath('//*[@class="giveaway-button"]')
        button.click()

    def submit_contact_info(self):
        button = self.browser.find_by_xpath(
            '//*[@class="giveaway-button-default"]'
        )
        button.click()

    def confirm_info(self):
        button = self.browser.find_by_xpath("//*[contains(@href, 'terms')]")
        button.click()

    def find_accept_button(self):
        return self.browser.find_by_xpath("//*[contains(@href, 'thanks')]")

class ContestEntry3(ContestEntry2):

    @staticmethod
    def mystyle(url):
        strs = "hummus kenra stiletto lillian chicco chanel anolon".split()
        return any(s in url for s in strs)

    def __init__(self, browser, url):
        super(ContestEntry3, self).__init__(browser, url)

    def click_submit(self):
        button = self.browser.find_by_xpath('//*[@class="giveaway-button"]')
        button.click()

    def submit_contact_info(self):
        button = self.browser.find_by_xpath(
            '//*[@class="giveaway-button-default"]'
        )
        button.click()

    def click_enter_now(self):
        button = self.browser.find_by_xpath(
            "//a[matches(@href, 'giveaway.*enter')]"
        )
        pdb.set_trace()
        button.click()

    def confirm_info(self):
        button = self.browser.find_by_xpath("//*[contains(@href, 'terms')]")
        button.click()

    def find_accept_button(self):
        return self.browser.find_by_xpath("//*[contains(@href, 'thanks')]")

    def enter_contest(self):
        print "\tEntering contest {0}".format(self.url)
        self.browser.visit(self.url)

        self.click_enter_now()

        self.enter_email()
        self.enter_contact_info()
        self.confirm_info()
        self.accept_terms()




def different_browser_flow(url):
    strs = "500-happy hummus kenra stiletto lillian chicco chanel anolon".split()
    return any(s in url for s in strs)

with Browser() as browser:

    initial_url = "http://www.sheknows.com/contests"
    browser.visit(initial_url)

    for url in contest_urls(browser):

        if ContestEntry.mystyle(url):
            pass #ContestEntry(browser, url).enter_contest()
        elif ContestEntry2.mystyle(url):
            pass #ContestEntry2(browser, url).enter_contest()
        elif ContestEntry3.mystyle(url):
            ContestEntry3(browser, url).enter_contest()
        else:
            print "Ignoring {0}".format(url)
