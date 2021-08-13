#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 11:28:38 2021

@author: katebelisle
"""

import PyPDF2
import datetime

#%% wget https://www.effinghamnh.net/wp-content/uploads/2012/01/junkyard-ordinance.pdf
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
junkyard_ordinance="junkyard-ordinance.pdf"
pdf_reader = PyPDF2.PdfFileReader(junkyard_ordinance)
print(f'Number of Pages in PDF File is {pdf_reader.getNumPages()}')
print(f'PDF Metadata is {pdf_reader.documentInfo}')
print(f'PDF File Author is {pdf_reader.documentInfo["/Author"]}')
print(f'PDF File Creator is {pdf_reader.documentInfo["/Creator"]}')
#%% Examine Date
text_date = pdf_reader.documentInfo["/ModDate"]
print(text_date)
text_date = text_date.replace("'", "")
text_date = text_date.replace("D:", "")
text_date = text_date.replace("0000", "")
file_date = datetime.datetime.strptime(text_date, "%Y%m%d%H%M%S%z")
print (file_date.strftime(fmt))