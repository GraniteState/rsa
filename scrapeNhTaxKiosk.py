#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:07:16 2021

@author: katebelisle
"""

import re
import urlparse
import mechanize

url = "http://www.searchiqs.com/nybro/"
driver = webdriver.PhantomJS()
driver.get(url)
driver.find_element_by_name('btnGuestLogin').click()
driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtName').send_keys('david')
driver.find_element_by_name('ctl00$ContentPlaceHolder1$cmdSearch').click()