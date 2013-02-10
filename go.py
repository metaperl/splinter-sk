#!/usr/bin/python

import pdb

from splinter import Browser

base_url = 'http://www.sheknows.com'

user = dict(
    first_name = "Terrence",
    last_name = "Brannon",
    phone_number = "818-359-0893",
    address = "713 Chadford Rd",
    city = "Irmo",
    state = "usa-sc",
    zip = "29063"
)


def contest_url(path):
    return "{0}{1}".format(base_url,path)

def contest_urls(browser):
    contests = browser.find_by_xpath('//*[@id="carousel_list"]/li')
    return [contest_url(contest['data-url']) for contest in contests]

def click_submit():
    button = browser.find_by_xpath('//*[@class="submit button"]')
    button.click()

def enter_email(url):
    browser.visit(url)
    browser.fill("data[GiveawayEntry][email]", 'schemelab@gmail.com')
    click_submit()

def enter_contact_info(url):
    for k, v in user.items():
        if k == 'state': continue
        field_name = "data[GiveawayEntry][{0}]".format(k)
        if k == 'address' or k == 'city' or k == 'zip':
            field_name = "data[GiveawayEntryAddress][{0}]".format(k)
        browser.fill(field_name, v)
    e = browser.find_by_xpath(
        '//*[@value="{0}"]'.format(user['state'])
    )
    e._element.click()
    click_submit()

def confirm_info():
    browser.find_by_xpath('//*[@class="button button-yes"]').click()

def accept_terms():
    browser.find_by_xpath('//*[@class="button"]').click()

def enter_contest(u):
    enter_email(u)
    enter_contact_info(u)
    confirm_info()
    accept_terms()
    pdb.set_trace()

with Browser() as browser:
    # Visit URL
    url = "http://www.sheknows.com/contests"
    browser.visit(url)

    for u in contest_urls(browser):
        enter_contest(u)


    if browser.is_text_present('splinter.cobrateam.info'):
        print "Yes, the official website was found!"
    else:
        print "No, it wasn't found... We need to improve our SEO techniques"
