import base64
import os
import pyconfluence
from pyconfluence.actions import edit_page,get_page_content


def set_confluence_environment():
    os.environ['PYCONFLUENCE_TOKEN'] = base64.b64decode( os.environ['AUTH'].encode( 'utf-8' ) ).decode( 'utf-8' ).split(':')[1].strip()
    os.environ['PYCONFLUENCE_USER'] = 'j1013225'
    os.environ['PYCONFLUENCE_URL'] = 'https://confluence.jda.com'


def update_lifelist_page(xhtml):
    set_confluence_environment()
    edit_page('154903335', 'What am I doing with my life', '~j1013225', xhtml)

def get_lifelist_page_contents():
    set_confluence_environment()
    print(get_page_content('154903335'))
       