import base64
import os
import pyconfluence
from pyconfluence.actions import get_page_content


def update_lifelist_page(xhtml):
    pass
    
os.environ['PYCONFLUENCE_TOKEN'] = base64.b64decode( os.environ['AUTH'].encode( 'utf-8' ) ).decode( 'utf-8' ).split(':')[1].strip()
os.environ['PYCONFLUENCE_USER'] = 'j1013225'
os.environ['PYCONFLUENCE_URL'] = 'https://confluence.jda.com'


print(get_page_content('154903335'))