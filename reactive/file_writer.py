from charms.reactive import when, when_not, set_flag, endpoint_from_flag
from charmhelpers.core import hookenv

import os
import PyPDF2
import requests
from random import random

CHARM_DOC = '/home/ubuntu/charm_doc.txt'
URL = 'https://media.readthedocs.org/pdf/charmsreactive/latest/charmsreactive.pdf' 

def return_rand_page(pdf):
    pdf_file = open(pdf, 'rb')
    reader = PyPDF2.PdfFileReader(pdf_file) 
    num_pages = reader.numPages
    rand_page = random.randint(1, num_pages)
    pdf_page = reader.getPage(rand_page)

    return pdf_page


def write_file(page):
    with open(CHARM_DOC, 'a+') as f:
        f.write(page)

@when_not('file_writer.available')
def get_and_write():
    hookenv.status_set('active', 'Creating File Dir')
    pdf = requests.get(URL)
    rand_page = return_rand_page(pdf)
    write_file(rand_page)
    set_flag('file-writer.available')


@when('file-writer.available')
def repeat():
    clear_flag('file-writer.available')


        
