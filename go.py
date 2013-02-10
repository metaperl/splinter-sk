#!/usr/bin/python

import pdb

from splinter import Browser

base_url = 'http://www.sheknows.com'

user = dict(
    first_name = "Terrence",
    last_name = "Brannon",
    phone = "818-359-0893",
    address = "713 Chadford Rd",
    city = "Irmo",
    state = "usa-sc",
    zip = "29063"
)

user_to


def contest_url(path):
    return "{0}{1}".format(base_url,path)

def contest_urls(browser):
    contests = browser.find_by_xpath('//*[@id="carousel_list"]/li')
    for contest in contests:
        yield contest_url(contest['data-url'])

def click_submit():
    button = browser.find_by_xpath('//*[@class="submit button"]')
    button.click()

def enter_email(url):
    browser.visit(url)
    browser.fill("data[GiveawayEntry][email]", 'schemelab@gmail.com')
    click_submit()

def enter_contest(u):
    enter_email(u)

with Browser() as browser:
    # Visit URL
    url = "http://www.sheknows.com/contests"
    browser.visit(url)

    for u in contest_urls(browser):
        enter_contest(u)

    # Interact with elements
    button.click()
    if browser.is_text_present('splinter.cobrateam.info'):
        print "Yes, the official website was found!"
    else:
        print "No, it wasn't found... We need to improve our SEO techniques"
